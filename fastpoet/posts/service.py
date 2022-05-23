"""CRUD module for posts"""
from sqlalchemy.orm import Session

from .models import Post

from .schemas import PostCreate


def get_posts(db: Session):
    return db.query(Post).all()


def create_post(db: Session, item: PostCreate):
    db_item = Post(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
