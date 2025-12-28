import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
from jose import jwt
from .config import settings

class Hasher:
    """
    Simplified manager for debugging. Hashing is disabled.
    """
    def __init__(self):
        pass

    def get_password_hash(self, password: str) -> str:
        """Returns the password as-is (NO HASHING)."""
        return password

    def verify_password(self, plain_password: str, stored_password: str) -> bool:
        """Performs direct string comparison."""
        return plain_password == stored_password

    def get_copyparty_hash(self, text: str) -> str:
        """Returns the text as-is (NO HASHING)."""
        return text

    def derive_key(self, secret: str) -> bytes:
        """Derives a 32-byte key using SHA-256."""
        return hashlib.sha256(secret.encode()).digest()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Creates a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

# Singleton instance
hasher = Hasher()