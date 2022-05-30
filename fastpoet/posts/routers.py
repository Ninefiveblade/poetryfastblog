"""Routing module for posts"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastpoet.settings.database import engine, get_db

from ..groups.service import get_group
from .models import Post
from .schemas import PostCreate, PostList
from .service import create_post, get_posts

router = APIRouter()


@router.get("/posts/", response_model=list[PostList])
def posts_get(db: Session = Depends(get_db)):
    posts = get_posts(db)
    return posts


@router.post("/posts/", response_model=PostCreate)
def post_create(post: PostCreate, db: Session = Depends(get_db)):
    """Create new post"""
    if post.group_id:
        if not get_group(db, post.group_id):
            raise HTTPException(
                status_code=404,
                detail=f"Группа под номером: {post.group_id} не существует.")
    # Нужна проверка что переданный author_id есть в db
    post = create_post(db, post)
    return post
