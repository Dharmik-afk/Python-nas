from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# The database URL is read from the configuration
# For SQLite, it will look like: "sqlite:///./data/server.db"
engine = create_engine(
    settings.DATABASE_URL,
    # connect_args is needed only for SQLite to allow multi-threaded access
    connect_args={"check_same_thread": False},
)

# SessionLocal will be the session class used for all database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
