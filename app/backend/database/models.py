from sqlalchemy import Boolean, Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) # Bcrypt hash for DB auth
    cp_hash = Column(String, nullable=True)         # SHA-512 hash for Copyparty
    permissions = Column(String, default="r") 
    is_active = Column(Boolean, default=True)

    # In the future, you could add relationships here, for example:
    # items = relationship("Item", back_populates="owner")
