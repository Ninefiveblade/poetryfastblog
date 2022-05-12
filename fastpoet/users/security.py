from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .service import get_user_by_username
from fastpoet.settings import models
from .routers import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

User = models.User


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(username: str, db: Session = Depends(get_db)):
    if username in db:
        user_dict = get_user_by_username(username)
        return UserInDB(**user_dict)


class UserInDB(User):
    hashed_password: str


def fake_decode_token(token):
    user = get_user(get_db(), token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
