"""Routing module for users"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastpoet.settings import models
from fastpoet.settings.database import SessionLocal, engine

from .schemas import User, UserCreate
from .service import create_user, get_user, get_users

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/users/", response_model=list[User])
def users_get(db: Session = Depends(get_db)):
    users = get_users(db)
    return users


@router.get("/users/{user_id}", response_model=User)
def user_get(user_id: int, db: Session = Depends(get_db)):
    users = get_user(db, user_id)
    return users
