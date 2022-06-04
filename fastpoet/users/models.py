"""Models for users."""
import datetime

from sqlalchemy import (Boolean, Column, DateTime, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from fastpoet.settings.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    born_year = Column(Integer, index=True, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=True)
    is_user = Column(Boolean, default=False)
    posts = relationship(
        "Post", cascade="all, delete-orphan", back_populates="author"
    )

    __table_args__ = (
        UniqueConstraint("username", "first_name", name="unique_username"),
    )
