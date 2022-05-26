"""Models for users."""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from fastpoet.settings.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    posts = relationship("Post", back_populates="author")
