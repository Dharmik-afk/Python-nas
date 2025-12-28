import os
from pydantic import BaseSettings, validator
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # Project base directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    # Server Configuration
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: Path = BASE_DIR / "logs" / "server.log"
    # Secret key for signing tokens
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Session Configuration
    SESSION_MAX_COUNT: int = 1000
    SESSION_TIMEOUT_SECONDS: int = 86400

    # Database configuration
    DATABASE_URL: str = f"sqlite:///{Path(__file__).resolve().parent.parent.parent}/storage/db/server.db"

    # Copyparty Backend Configuration
    COPYPARTY_PORT: int = 8090
    COPYPARTY_ADMIN_USER: str = "admin"
    COPYPARTY_ADMIN_PASS: str = "admin_pass_a7b3c9d1e5f"

    # Directory to serve files from
    CUSTOM_SERVE_DIR: Optional[str] = os.getenv("CUSTOM_SERVE_DIR")
    SERVE_DIR: str = ""

    @property
    def SERVE_PATH(self) -> Path:
        return Path(self.SERVE_DIR)

    @validator("SERVE_DIR", always=True, pre=True)
    def set_serve_dir(cls, v, values):
        # Prioritize CUSTOM_SERVE_DIR from environment or values
        custom = values.get("CUSTOM_SERVE_DIR") or os.getenv("CUSTOM_SERVE_DIR")
        if custom:
            return str(Path(custom.strip()).resolve())
        # Default to media folder in project root
        base_dir = Path(__file__).resolve().parent.parent.parent
        return str((base_dir / "storage" / "files").resolve())

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single settings instance to be used across the application
settings = Settings()
