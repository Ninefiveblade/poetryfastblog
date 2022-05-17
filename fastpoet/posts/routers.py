"""Routing module for posts"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastpoet.settings import models
from fastpoet.settings.database import engine, get_db

from .schemas import PostCreate, PostList
from .service import create_post, get_posts

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.get("/posts/", response_model=list[PostList])
def posts_get(db: Session = Depends(get_db)):
    posts = get_posts(db)
    return posts


@router.post("/posts/", response_model=PostCreate)
def post_create(post: PostCreate, db: Session = Depends(get_db)):
    """Create new post"""
    # Нужна проверка что переданный author_id есть в db
    post = create_post(db, post)
    return post
