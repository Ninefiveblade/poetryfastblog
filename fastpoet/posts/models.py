"""Models module for posts"""
import sqlalchemy as sa
from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastpoet.settings.database import Base



class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    slug = Column(String, index=True)


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    slug = Column(String, index=True)


association_table = Table(
    "association",
    Base.metadata,
    Column("category_id", ForeignKey("category.id")),
    Column("genre_id", ForeignKey("genre.id")),
)


class Title(Base):
    __tablename__ = 'title'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    year = Column(Integer, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    #category = relationship("Category", secondary=association_table)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    #genre = relationship("Genre", secondary=association_table)
    description = Column(String)


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey("title.id"))
    title = relationship(
        'Title', back_populates='review',
        lazy='dynamic', cascade='all, delete-orphan'
    )
    score = Column(Integer)
    text = Column(String, index=True)
    pub_date = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship(
        'User', back_populates='review',
        lazy='dynamic', cascade='all, delete-orphan'
    )


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey("review.id"))
    review = relationship(
        'Review', back_populates='comments',
        lazy='dynamic', cascade='all, delete-orphan'
    )
    text = Column(String, index=True)
    pub_date = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship(
        'User', back_populates='comments',
        lazy='dynamic', cascade='all, delete-orphan'
    )
