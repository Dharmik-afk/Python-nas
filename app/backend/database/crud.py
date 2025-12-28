import logging
from sqlalchemy.orm import Session
from . import models
from app.backend.models import user_schemas
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)

def get_user_by_username(db: Session, username: str):
    """Fetches a user by their username."""
    logger.debug(f"Querying for user: {username}")
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: user_schemas.UserCreate):
    """Creates a new user in the database."""
    logger.info(f"Creating new user: {user.username}")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Successfully created user {user.username} with ID {db_user.id}")
    return db_user