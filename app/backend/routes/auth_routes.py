import logging
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import get_basic_auth_header, encrypt_string, verify_password
from app.core.security import create_access_token
from app.core.session_manager import session_manager
from app.backend.database.session import SessionLocal
from app.backend.database.models import User
from app.backend.models.user_schemas import Token

router = APIRouter(prefix="/api/v1/auth")
logger = logging.getLogger(__name__)

@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == form_data.username, User.is_active == True).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        # Create a session to store the copyparty auth header (proxy requirement)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        session = session_manager.create_session(client_ip, user_agent)
        
        auth_header = get_basic_auth_header(user.username, form_data.password)
        session.username = user.username
        session.auth_header = encrypt_string(auth_header)
        session.log_activity(f"User '{user.username}' logged in via API.")
        session_manager.save_sessions()

        # Create JWT pointing to this session
        access_token = create_access_token(data={"sub": user.username, "session_id": session.session_id})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), remember_me: Optional[str] = Form(None)):
    """Handles user login for the frontend (Browser/HTMX)."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username, User.is_active == True).first()
        
        if user and verify_password(password, user.hashed_password):
            # Reuse existing session if possible, or create new
            session = getattr(request.state, "session", None)
            if not session:
                client_ip = request.client.host if request.client else "unknown"
                user_agent = request.headers.get("user-agent", "unknown")
                session = session_manager.create_session(client_ip, user_agent)
            
            # For proxying to Copyparty, we still need the Basic Auth header.
            auth_header = get_basic_auth_header(username, password)
            
            session.username = username
            session.auth_header = encrypt_string(auth_header)
            session.log_activity(f"User '{username}' logged in.")
            
            session_manager.save_sessions()
            
            # Generate JWT
            access_token = create_access_token(data={"sub": username, "session_id": session.session_id})
            
            response = JSONResponse(content={"message": "Login successful", "username": username, "token": access_token})
            
            # Robust boolean check
            is_remember = remember_me and remember_me.lower() in ("true", "on", "1", "yes")
            max_age = 30 * 24 * 3600 if is_remember else 3600 # 30 days or 1 hour
            
            # Set JWT Cookie
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="lax",
                secure=False, # Set to True in production with HTTPS
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
            logger.warning(f"Failed login attempt for user: {username}")
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
