"""CRUD module for users"""
from datetime import datetime, timedelta
from typing import Union

from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status

from fastpoet.settings.models import User
from fastpoet.settings import security_config
from .schemas import UserCreate, UserInDB, TokenData
from .security import get_password_hash, verify_password, oauth2_scheme

def add_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_token(db: Session, username: str): # получаем юзера
    '''Для токена.'''
    user = db.query(User).filter(User.username == username).first()
    if user:
        user_dict = user.__dict__
        return UserInDB(**user_dict)


def authenticate_user(db: Session, username: str, password: str): # "авторизируем" пользователя
    user = get_user_token(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password): # проверяем пароли
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None): # создаем токен
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, security_config.SECRET_KEY,
        algorithm=security_config.ALGORITHM
    )
    return encoded_jwt


def get_current_user( # проверим токен юзера, пока не юзается
    db: Session,
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security_config.SECRET_KEY,
            algorithms=[security_config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_token(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
