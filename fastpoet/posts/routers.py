"""Routing module for posts"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastpoet.settings import models
from fastpoet.settings.database import engine

from .schemas import Post, PostCreate
from .service import create_post, get_posts
from fastpoet.settings.database import get_db

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.get("/posts/", response_model=list[Post])
def posts_get(db: Session = Depends(get_db)):
    posts = get_posts(db)
    return posts


@router.post("/posts/", response_model=Post)
def posts_create(
    user_id: int,
    post: PostCreate,
    db: Session = Depends(get_db)
):
    posts = create_post(db, post, user_id)
    return posts
