import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
from jose import jwt
from passlib.context import CryptContext
from .config import settings

class Hasher:
    """
    Unified hashing and token manager.
    Step 1 Removal: Plain-text proxying to Copyparty.
    """
    def __init__(self):
        # Standard secure hashing for the SQLite DB (Keep this enabled)
        self.pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        """Hashes a plain password for DB storage."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against a hashed one."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_internal_proxy_password(self, plain_password: str) -> str:
        """
        Returns the raw password for internal proxying.
        (Hashing removed for Step 1 of debugging)
        """
        return plain_password

    def get_copyparty_hash(self, internal_pw: str) -> str:
        """
        Returns the password as-is.
        (Copyparty custom hashing removed for Step 1 of debugging)
        """
        return internal_pw

    def derive_key(self, secret: str) -> bytes:
        return hashlib.sha256(secret.encode()).digest()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

hasher = Hasher()