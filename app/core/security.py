import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from .config import settings

# Use passlib for password hashing
# Note: switched to sha256_crypt because of compatibility issues between 
# passlib 1.7.4 and bcrypt 4.x/5.x on some systems (like Termux).
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def get_copyparty_hash(password: str) -> str:
    """
    Returns the SHA-512 hash for Copyparty, prefixed with +.
    Uses 424242 iterations to match --ah-alg sha2,424242
    """
    # Note: Copyparty's 'sha2' with iterations uses PBKDF2-SHA512
    import hashlib
    h = hashlib.pbkdf2_hmac('sha512', password.encode(), b'', 424242)
    return "+" + base64.urlsafe_b64encode(h).decode().rstrip('=')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
