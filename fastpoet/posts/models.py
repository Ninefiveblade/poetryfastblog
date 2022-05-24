"""Models module for posts"""
import sqlalchemy as sa
from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastpoet.settings.database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), index=True, unique=True)
    slug = Column(String(50), index=True, unique=True)
    
    genres = relationship(
        'Genre', secondary='title', back_populates='categories'
    )


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), index=True, unique=True)
    slug = Column(String(50), index=True, unique=True)
    categories = relationship(
        'Category', secondary='title', back_populates='genres'
    )


class Title(Base):
    __tablename__ = 'title'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, index=True)
    year = Column(Integer, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    description = Column(String)


# class Review(Base):
#     __tablename__ = 'review'

#     id = Column(Integer, primary_key=True)
#     title_id = Column(Integer, ForeignKey("title.id"))
#     title = relationship(
#         'Title', back_populates='review',
#         lazy='dynamic', cascade='all, delete-orphan'
#     )
#     score = Column(Integer)
#     text = Column(String, index=True)
#     pub_date = Column(DateTime, server_default=func.now())
#     author_id = Column(Integer, ForeignKey("users.id"))
#     author = relationship(
#         'User', back_populates='review',
#         lazy='dynamic', cascade='all, delete-orphan'
#     )


# class Comments(Base):
#     __tablename__ = 'comments'

#     id = Column(Integer, primary_key=True)
#     review_id = Column(Integer, ForeignKey("review.id"))
#     review = relationship(
#         'Review', back_populates='comments',
#         lazy='dynamic', cascade='all, delete-orphan'
#     )
#     text = Column(String, index=True)
#     pub_date = Column(DateTime, server_default=func.now())
#     author_id = Column(Integer, ForeignKey("users.id"))
#     author = relationship(
#         'User', back_populates='comments',
#         lazy='dynamic', cascade='all, delete-orphan'
#     )
