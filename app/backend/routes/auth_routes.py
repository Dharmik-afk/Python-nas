import logging
import requests
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import get_basic_auth_header, encrypt_string
from app.core.security import hasher
from app.core.config import settings
from app.core.session_manager import session_manager
from app.backend.database.session import SessionLocal
from app.backend.database.models import User
from app.backend.models.user_schemas import Token

router = APIRouter(prefix="/api/v1/auth")
logger = logging.getLogger(__name__)

def verify_with_copyparty(username: str, hashed_pw: str) -> bool:
    """Performs a handshake verification with the Copyparty backend."""
    try:
        url = f"http://127.0.0.1:{settings.COPYPARTY_PORT}/?pmask"
        auth = (username, hashed_pw)
        response = requests.get(url, auth=auth, timeout=5)
        
        print(f"\n[Handshake] Copyparty Verification for '{username}':")
        print(f" > Status: {response.status_code}")
        print(f" > Body: {response.text.strip()}")
        
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Copyparty handshake failed: {e}")
        return False

@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == form_data.username, User.is_active == True).first()
        if not user or not hasher.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        # New: Verify with Copyparty Backend
        if not verify_with_copyparty(user.username, user.hashed_password):
            logger.error(f"Login rejected: Copyparty backend did not authorize user '{user.username}'")
            raise HTTPException(status_code=502, detail="Backend file server synchronization error.")

        # Create a session to store the copyparty auth header (proxy requirement)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        session = session_manager.create_session(client_ip, user_agent)
        
        # Calculate internal proxy credential
        internal_pw = hasher.get_internal_proxy_password(form_data.password)
        
        # New: Verify with Copyparty Backend
        if not verify_with_copyparty(user.username, internal_pw):
            logger.error(f"Login rejected: Copyparty backend did not authorize user '{user.username}'")
            raise HTTPException(status_code=502, detail="Backend file server synchronization error.")

        # Create a session to store the copyparty auth header (proxy requirement)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        session = session_manager.create_session(client_ip, user_agent)
        
        # Use the internal proxy password for Copyparty authentication
        auth_header = get_basic_auth_header(user.username, internal_pw)
        session.username = user.username
        session.auth_header = encrypt_string(auth_header)
        session.log_activity(f"User '{user.username}' logged in via API.")
        session_manager.save_sessions()

        # Create JWT pointing to this session
        access_token = hasher.create_access_token(data={"sub": user.username, "session_id": session.session_id})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()

@router.post("/login")
async def login(
    request: Request, 
    username: Optional[str] = Form(None), 
    password: Optional[str] = Form(None), 
    remember_me: Optional[str] = Form(None)
):
    """Handles user login for the frontend (Browser/HTMX)."""
    logger.debug(f"Login attempt. Content-Type: {request.headers.get('content-type')}")
    
    # Fallback to JSON if Form data is missing
    if not username or not password:
        try:
            data = await request.json()
            username = username or data.get("username")
            password = password or data.get("password")
            remember_me = remember_me or data.get("remember_me")
        except Exception:
            pass

    if not username or not password:
        raise HTTPException(
            status_code=422, 
            detail=[{"loc": ["body", "username"], "msg": "field required", "type": "value_error.missing"}]
        )

    db = SessionLocal()
    try:
        # Debug: check all users in DB
        all_users = db.query(User).all()
        logger.debug(f"DB Check: Found {len(all_users)} users in database. Incoming username: {repr(username)}")
        
        user = db.query(User).filter(User.username == username.strip() if username else None, User.is_active == True).first()
        
        if user:
            is_valid = hasher.verify_password(password, user.hashed_password)
            if is_valid:
                logger.info(f"DEBUG LOGIN SUCCESS: User '{username}' successfully authenticated.")
                
                # Calculate internal proxy credential
                internal_pw = hasher.get_internal_proxy_password(password)

                # New: Verify with Copyparty Backend
                if not verify_with_copyparty(user.username, internal_pw):
                    logger.error(f"Login rejected: Copyparty backend did not authorize user '{user.username}'")
                    raise HTTPException(status_code=502, detail="Backend file server synchronization error.")

                # Reuse existing session if possible, or create new
                session = getattr(request.state, "session", None)
                if not session:
                    client_ip = request.client.host if request.client else "unknown"
                    user_agent = request.headers.get("user-agent", "unknown")
                    session = session_manager.create_session(client_ip, user_agent)
                
                # For proxying to Copyparty, we use the internal proxy password
                auth_header = get_basic_auth_header(user.username, internal_pw)
                
                session.username = user.username
                session.auth_header = encrypt_string(auth_header)
                session.log_activity(f"User '{user.username}' logged in.")
                
                session_manager.save_sessions()
                
                # Generate JWT
                access_token = hasher.create_access_token(data={"sub": user.username, "session_id": session.session_id})
                
                response = JSONResponse(content={"message": "Login successful", "username": user.username, "token": access_token})
                
                # Robust boolean check
                is_remember = remember_me and remember_me.lower() in ("true", "on", "1", "yes")
                max_age = 30 * 24 * 3600 if is_remember else 3600 # 30 days or 1 hour
                
                # Set JWT Cookie
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    samesite="lax",
                    secure=False,
                    max_age=max_age
                )
                
                # Maintain legacy session_id cookie for now (optional, but safe)
                response.set_cookie(
                    key="session_id",
                    value=session.session_id,
                    httponly=True,
                    samesite="lax",
                    secure=False,
                    max_age=max_age
                )
                    
                return response
            else:
                logger.error(f"DEBUG LOGIN FAILURE: User '{username}' provided password '{password}', but hash in DB is '{user.hashed_password}'")
                raise HTTPException(status_code=401, detail="Invalid username or password")
        else:
            logger.warning(f"Login attempt for non-existent or inactive user: {username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
    finally:
        db.close()


@router.post("/logout")
async def logout(request: Request):
    """Logs out the user by clearing their session data."""
    session = getattr(request.state, "session", None)
    if session:
        session.username = None
        session.auth_header = None
        session.log_activity("User logged out.")
        session_manager.save_sessions()
    
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("access_token")
    response.delete_cookie("session_id")
    return response