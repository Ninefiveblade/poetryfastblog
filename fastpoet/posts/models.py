"""Models module for posts."""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastpoet.users.models import User
from fastpoet.groups.models import Group
from fastpoet.settings.database import Base


class Post(Base):
    """Модель поста."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey(Group.id))

    author = relationship(User, back_populates="posts")
    group = relationship(Group, back_populates="posts")
