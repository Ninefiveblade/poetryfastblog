"""Routing module for posts"""
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from fastpoet.settings import models
from . import service, schemas

from fastpoet.settings.database import SessionLocal, engine

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/posts/", response_model=list[schemas.Post])
def posts_get(db: Session = Depends(get_db)):
    posts = service.get_posts(db)
    return posts


@router.post("/posts/", response_model=schemas.Post)
def posts_create(
    user_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    posts = service.create_post(db, post, user_id)
    return posts
