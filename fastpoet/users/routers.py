"""Routing module for users"""
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from . import service, schemas
from fastpoet.settings import models
from fastpoet.settings.database import SessionLocal, engine

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def users_get(db: Session = Depends(get_db)):
    users = service.get_users(db)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def user_get(user_id: int, db: Session = Depends(get_db)):
    users = service.get_user(db, user_id)
    return users
