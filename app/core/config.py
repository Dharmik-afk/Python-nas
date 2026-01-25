import os
import secrets
from pydantic import BaseSettings, validator
from pathlib import Path
from typing import Optional
from .utils import get_lan_ip

class Settings(BaseSettings):
    # Project base directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # Debug Mode
    DEBUG: bool = False

    # Server Configuration
    FRONTEND_PORT: int = 8000
    FRONTEND_HOST: str = "0.0.0.0"

    # CORS Configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8081", # Typical React Native Metro Bundler
        "http://127.0.0.1",
    ]

    @validator("FRONTEND_HOST", always=True, pre=True)
    def set_frontend_host(cls, v, values):
        # If explicitly set in .env and it's not the generic 0.0.0.0, respect it
        if v and v != "0.0.0.0":
            return v
        # Default based on DEBUG: localhost for debug, 0.0.0.0 (All interfaces) for production
        if values.get("DEBUG"):
            return "127.0.0.1"
        else:
            return "0.0.0.0"

    @property
    def FRONTEND_IP(self) -> str:
        """
        Returns the LAN IP for production or 127.0.0.1 for debug mode.
        Used for display purposes.
        """
        if self.DEBUG:
            return "127.0.0.1"
        return "0.0.0.0"

    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: Path = BASE_DIR / "logs" / "server.log"
    # Secret key for signing tokens
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours

    # Session Configuration
    SESSION_MAX_COUNT: int = 1000
    SESSION_TIMEOUT_SECONDS: int = 86400

    # Database configuration
    DATABASE_URL: str = f"sqlite:///{Path(__file__).resolve().parent.parent.parent}/storage/db/server.db"

    # Copyparty Backend Configuration
    COPYPARTY_HOST: str = "127.0.0.1"
    COPYPARTY_PORT: int = 8090
    COPYPARTY_ADMIN_USER: str = "admin"
    COPYPARTY_ADMIN_PASS: Optional[str] = None

    # Directory to serve files from
    CUSTOM_SERVE_DIR: Optional[str] = None
    SERVE_DIR: str = ""

    # Path Security
    RESTRICTED_DIRS: list[Path] = []
    ALLOWED_OVERRIDE_DIRS: list[Path] = []

    @property
    def SERVE_PATH(self) -> Path:
        return Path(self.SERVE_DIR)

    @validator("RESTRICTED_DIRS", always=True, pre=True)
    def set_restricted_dirs(cls, v, values):
        base_dir = values.get("BASE_DIR") or Path(__file__).resolve().parent.parent.parent
        return [
            base_dir,
            Path("/data/data/com.termux/files/usr/")
        ]

    @validator("ALLOWED_OVERRIDE_DIRS", always=True, pre=True)
    def set_allowed_override_dirs(cls, v, values):
        base_dir = values.get("BASE_DIR") or Path(__file__).resolve().parent.parent.parent
        return [
            base_dir / "storage" / "files"
        ]

    @validator("SECRET_KEY", always=True, pre=True)
    def set_secret_key(cls, v, values):
        # If the key is the insecure default or missing, try to load/generate a persistent one
        if v == "your-secret-key-here" or not v:
            # We need BASE_DIR. Since validators run in order, and BASE_DIR is defined first,
            # it might be in values. But BASE_DIR has a default, so we can re-compute it if needed.
            base_dir = values.get("BASE_DIR") or Path(__file__).resolve().parent.parent.parent
            secret_file = base_dir / "storage" / "db" / ".secret"
            
            if secret_file.exists():
                return secret_file.read_text().strip()
            
            # Generate new key
            new_key = secrets.token_urlsafe(50)
            try:
                secret_file.parent.mkdir(parents=True, exist_ok=True)
                secret_file.write_text(new_key)
            except Exception:
                pass # If we can't write, we just use the in-memory key (will reset on restart)
            return new_key
        return v

    @validator("SERVE_DIR", always=True, pre=True)
    def set_serve_dir(cls, v, values):
        # Prioritize CUSTOM_SERVE_DIR loaded by Pydantic from .env/env
        custom = values.get("CUSTOM_SERVE_DIR")
        if custom:
            return str(Path(custom.strip()).expanduser().resolve())
        # Default to media folder in project root
        base_dir = Path(__file__).resolve().parent.parent.parent
        return str((base_dir / "storage" / "files").resolve())

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single settings instance to be used across the application
settings = Settings()
