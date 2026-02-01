import base64
import os
import hashlib
import hmac
import logging
from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    Fernet = None

from .config import settings
from .security import hasher
from .session_manager import session_manager, Session

logger = logging.getLogger(__name__)

# OAuth2 scheme for Swagger UI and API clients
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

def get_basic_auth_header(username, password):
    """Generates a Basic Authentication header string."""
    credentials = f"{username}:{password}"
    return "Basic " + base64.b64encode(credentials.encode()).decode()

class PurePythonCrypter:
    """
    A pure-python authenticated encryption implementation.
    Uses HMAC-SHA256 for integrity and a SHA256-based stream cipher for confidentiality.
    Used as a replacement when the 'cryptography' library is unavailable.
    """
    def __init__(self, key: bytes):
        # Derive a 32-byte internal key
        self.key = hashlib.sha256(key).digest()

    def _get_keystream(self, iv: bytes, length: int):
        keystream = b""
        counter = 0
        while len(keystream) < length:
            # Simple but effective keystream generation using HMAC
            keystream += hmac.new(self.key, iv + str(counter).encode(), hashlib.sha256).digest()
            counter += 1
        return keystream[:length]

    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode()
        iv = os.urandom(16)
        keystream = self._get_keystream(iv, len(data))
        ciphertext = bytes([b ^ k for b, k in zip(data, keystream)])
        
        # payload = version(1) + iv(16) + ciphertext(n)
        payload = b"\x01" + iv + ciphertext
        signature = hmac.new(self.key, payload, hashlib.sha256).digest()
        
        return base64.urlsafe_b64encode(payload + signature).decode()

    def decrypt(self, token: str) -> str:
        try:
            raw = base64.urlsafe_b64decode(token.encode())
            if len(raw) < 49: # 1 (ver) + 16 (iv) + 32 (sig)
                return ""
            
            payload, signature = raw[:-32], raw[-32:]
            
            # Verify signature first (EtM)
            if not hmac.compare_digest(hmac.new(self.key, payload, hashlib.sha256).digest(), signature):
                return ""
            
            if payload[0] != 1: # Check version
                return ""
            
            iv, ciphertext = payload[1:17], payload[17:]
            keystream = self._get_keystream(iv, len(ciphertext))
            return bytes([b ^ k for b, k in zip(ciphertext, keystream)]).decode()
        except Exception:
            return ""

def _get_crypter():
    key = hasher.derive_key(settings.SECRET_KEY)
    return PurePythonCrypter(key)

def _get_fernet() -> Optional[Fernet]:
    """Derives a 32-byte key from the SECRET_KEY for Fernet encryption."""
    if not HAS_CRYPTO:
        return None
    key = hasher.derive_key(settings.SECRET_KEY)
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_string(text: str) -> str:
    """Encrypts a string for storage in the session."""
    if not text:
        return ""
    
    if HAS_CRYPTO:
        f = _get_fernet()
        if f:
            try:
                return f.encrypt(text.encode()).decode()
            except Exception as e:
                logger.error(f"Fernet encryption failed: {e}")

    # Fallback to PurePythonCrypter
    return _get_crypter().encrypt(text)

def decrypt_string(encrypted_text: str) -> str:
    """Decrypts a string retrieved from the session."""
    if not encrypted_text:
        return ""

    # Try PurePythonCrypter first if it looks like one (starts with \x01 -> 'AQ' in b64)
    if encrypted_text.startswith("AQ"):
        decrypted = _get_crypter().decrypt(encrypted_text)
        if decrypted:
            return decrypted

    # Try Fernet if available
    if HAS_CRYPTO:
        f = _get_fernet()
        if f:
            try:
                return f.decrypt(encrypted_text.encode()).decode()
            except Exception:
                pass
    
    # Final fallback: try PurePythonCrypter even if it doesn't start with AQ
    # (in case of different base64 padding/encoding)
    decrypted = _get_crypter().decrypt(encrypted_text)
    if decrypted:
        return decrypted

    # If all fails, return as-is (might be plain text from previous workaround or dev)
    return encrypted_text

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
                    internal_pw = hasher.get_internal_proxy_password(password, user_salt=username)
                    proxy_auth_header = get_basic_auth_header(username, internal_pw)
                    
                    session.auth_header = encrypt_string(proxy_auth_header)
                    return session
            finally:
                db.close()
        except Exception:
            pass

    raise HTTPException(status_code=401, detail="Authentication required")
