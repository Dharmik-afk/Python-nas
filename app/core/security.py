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
        Returns the password for internal proxying.
        We now pass the plain password to Copyparty (or use it for hashing)
        as the previous SHA-256 workaround prevented correct hash alignment.
        """
        return plain_password

    def get_copyparty_hash(self, internal_pw: str) -> str:
        """
        Returns the Copyparty-compatible SHA-512 iterated hash.
        This matches Copyparty's custom 'sha2' algorithm.
        """
        # Default parameters from Copyparty
        salt = "HOnOz0yVP8H4WJncIu6Y8qof"
        iterations = 424242
        
        bplain = internal_pw.encode("utf-8")
        bsalt = salt.encode("utf-8")
        ret = b"\n"
        for _ in range(iterations):
            ret = hashlib.sha512(bsalt + bplain + ret).digest()

        return "+" + base64.urlsafe_b64encode(ret[:24]).decode("utf-8")

    def derive_key(self, secret: str) -> bytes:
        return hashlib.sha256(secret.encode()).digest()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

hasher = Hasher()