"""CRUD module for posts"""
from sqlalchemy.orm import Session

from .models import Group
from .schemas import GroupCreate


def get_groups(db: Session):
    return db.query(Group).all()


def create_group(db: Session, item: GroupCreate):
    db_item = Group(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
