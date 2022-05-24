"""CRUD module for posts"""
from sqlalchemy.orm import Session

from .models import Category, Genre, Title
from .schemas import CategoriesCreate, GenresCreate, TitlesCreate


def get_categories(db: Session):
    return db.query(Category).all()

def get_genres(db: Session):
    return db.query(Genre).all()

def get_titles(db: Session):
    return db.query(Title).all()


def create_categories(db: Session, item: CategoriesCreate):
    db_item = Category(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_genres(db: Session, item: GenresCreate):
    db_item = Genre(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_titles(db: Session, item: TitlesCreate):
    db_item = Title(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item