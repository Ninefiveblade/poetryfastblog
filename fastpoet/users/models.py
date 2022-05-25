"""Models for users."""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from fastapi_auth_middleware import FastAPIUser

from fastpoet.settings.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="author")


class CustomUser(FastAPIUser):
    def __init__(self, first_name: str, last_name: str, id: int, usename: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.usename = usename

    @property
    def identity(self) -> str:
        """ Identification attribute of the user """
        return self.id
