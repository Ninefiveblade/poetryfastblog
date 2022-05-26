"""Models module for groups."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from fastpoet.settings.database import Base


class Group(Base):
    """Group model."""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(String, index=True)

    posts = relationship("Post", back_populates="group")

