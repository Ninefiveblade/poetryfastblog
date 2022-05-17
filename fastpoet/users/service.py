"""CRUD module for users"""
from sqlalchemy.orm import Session

from fastpoet.settings.models import User

from .schemas import UserCreate, UserInDB
from .security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_token(db: Session, user_id: int):
    '''Для токена.'''
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user_dict = user.__dict__
        return UserInDB(**user_dict)


#  доделать
def fake_decode_token(db: Session, token):
    user = get_user(db, token)
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def add_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
