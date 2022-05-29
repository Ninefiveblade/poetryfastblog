"""Dependensies and CRUD for users."""
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import ValidationError

from fastpoet.settings import security_config
from .models import User
from .schemas import TokenData, UserCreate
from .security import get_password_hash, oauth2_scheme, verify_password


def add_user(db: Session, user: UserCreate):
    """Add new user to db"""
    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        born_year=user.born_year,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    """Grab user from db by id"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Grab user from db by username"""
    return db.query(User).filter(User.username == username).first()


def destroy_user_by_username(
    db: Session,
    username: str,
):
    """Delete user"""
    db.query(User).filter(User.username == username).delete()
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get users set"""
    return db.query(User).offset(skip).limit(limit).all()


def authenticate_user(db: Session, username: str, password: str) -> User:
    """Check user authentication"""
    user = get_user_by_username(db, username)
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


# протестировать скоупы
def get_current_user(
    security_scopes: SecurityScopes,
    db: Session, token: str = Depends(oauth2_scheme)
):
    """Get user by token and check"""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, security_config.SECRET_KEY,
            algorithms=[security_config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# crud для создания ролей 