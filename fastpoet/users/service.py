"""CRUD module for users"""
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from fastpoet.settings import security_config
from fastpoet.settings.models import User

from .schemas import TokenData, UserCreate
from .security import get_password_hash, oauth2_scheme, verify_password


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


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Функция проверяет аутентифицию пользователя"""
    user = get_user_by_username(db, username)
    if not user:
        return
    if not verify_password(password, user.hashed_password):
        return
    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
):
    """Функция создаёт токен"""
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


def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
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
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
