import base64
from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from cryptography.fernet import Fernet
from .config import settings
from .security import hasher
from .session_manager import session_manager, Session

# OAuth2 scheme for Swagger UI and API clients
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

def get_basic_auth_header(username, password):
    """Generates a Basic Authentication header string."""
    credentials = f"{username}:{password}"
    return "Basic " + base64.b64encode(credentials.encode()).decode()

def _get_fernet() -> Fernet:
    """Derives a 32-byte key from the SECRET_KEY for Fernet encryption."""
    key = hasher.derive_key(settings.SECRET_KEY)
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_string(text: str) -> str:
    """Encrypts a string for storage in the session."""
    if not text:
        return ""
    f = _get_fernet()
    return f.encrypt(text.encode()).decode()

def decrypt_string(encrypted_text: str) -> str:
    """Decrypts a string retrieved from the session."""
    if not encrypted_text:
        return ""
    f = _get_fernet()
    try:
        return f.decrypt(encrypted_text.encode()).decode()
    except Exception:
        return ""

async def auth_required(request: Request, token: Optional[str] = Depends(oauth2_scheme)) -> Session:
    """
    FastAPI dependency to ensure a user is logged in.
    Prioritizes JWT (Header -> Cookie) -> Session Cookie -> Basic Auth.
    Returns the Session object.
    """
    session = getattr(request.state, "session", None)
    
    # 1. JWT Authentication
    if not token:
        token = request.cookies.get("access_token")

    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            session_id = payload.get("session_id")
            if session_id:
                jwt_session = session_manager.get_session(session_id)
                if jwt_session and jwt_session.auth_header:
                    request.state.session = jwt_session
                    return jwt_session
        except JWTError:
            pass

    # 2. Existing Session Middleware
    if session and session.auth_header:
        return session

    # 3. Basic Auth (Fallback)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Basic "):
        try:
            from app.backend.database.session import SessionLocal
            from app.backend.database.models import User
            
            encoded_creds = auth_header.split(" ")[1]
            decoded_creds = base64.b64decode(encoded_creds).decode()
            username, password = decoded_creds.split(":", 1)
            
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.username == username, User.is_active == True).first()
                if user and hasher.verify_password(password, user.hashed_password):
                    if not session:
                         client_ip = request.client.host if request.client else "unknown"
                         user_agent = request.headers.get("user-agent", "unknown")
                         session = session_manager.create_session(client_ip, user_agent)
                         request.state.session = session
                    
                    session.username = username
                    
                    # Fix: Calculate internal proxy credential from the raw password
                    internal_pw = hasher.get_internal_proxy_password(password)
                    proxy_auth_header = get_basic_auth_header(username, internal_pw)
                    
                    session.auth_header = encrypt_string(proxy_auth_header)
                    return session
            finally:
                db.close()
        except Exception:
            pass

    raise HTTPException(status_code=401, detail="Authentication required")