"""Dependensies and CRUD for users."""
from datetime import datetime, timedelta
from typing import Union

from jose import jwt
from sqlalchemy.orm import Session

from fastpoet.settings import security_config

from fastpoet.users.models import User
from fastpoet.users.security import verify_password
from fastpoet.users.crud import crud_user


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Check user authentication"""
    user = crud_user.get_user_by_username(db, username)
    if not user:
        return
    if not verify_password(password, user.hashed_password):
        return
    return user


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
):
    """Create a token for user"""
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
