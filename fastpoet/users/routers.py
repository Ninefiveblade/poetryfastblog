"""Routing module for users"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from fastpoet.settings.database import engine
from .schemas import User, UserCreate
from .service import add_user, get_user, get_users
from fastpoet.settings.database import get_db
from fastpoet.settings import models

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.get("/users/", response_model=list[User])
def users_get(db: Session = Depends(get_db)):
    """Get users"""
    users = get_users(db)
    return users


@router.get("/users/{user_id}", response_model=User)
def user_get(user_id: int, db: Session = Depends(get_db)):
    """Get user by id"""
    user = get_user(db, user_id)
    return user


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create new user"""
    return add_user(db=db, user=user)


@router.get("/test/")
def get_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return {"token": token}
