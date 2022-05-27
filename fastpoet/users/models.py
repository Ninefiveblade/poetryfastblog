"""Models for users."""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from fastpoet.settings.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    born_year = Column(Integer, index=True, default=None)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    posts = relationship(
        "Post", cascade="all, delete-orphan", back_populates="author"
    )
