"""Secure depends for users."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from fastpoet.settings import security_config

from .crud import crud_user
from .schemas import token_schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token/",
)


def get_password_hash(password: str) -> str:
    """Create hashed user password."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Check plain password with hashed, return Bool."""
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    """Get user by token and check"""
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
        token_data = token_schema.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = crud_user.get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
