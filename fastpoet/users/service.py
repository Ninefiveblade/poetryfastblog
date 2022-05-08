"""CRUD module for users"""

from sqlalchemy.orm import Session

from fastpoet.settings import models

from .schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


# лимиты на количество записей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    # тут видимо будет защита паролей.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
