"""Routing module for posts."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.groups.service import get_group
from fastpoet.posts.models import Post
from fastpoet.settings.database import get_db

from .schemas import PostCreate, PostList
from .service import create_post, get_posts

router = APIRouter()


@router.get(
    "/posts/", response_model=List[PostList], status_code=status.HTTP_200_OK
)
def posts_get(db: Session = Depends(get_db)) -> List[PostList]:
    return get_posts(db)


@router.post(
    "/posts/", response_model=PostCreate, status_code=status.HTTP_201_CREATED
)
def post_create(post: PostCreate, db: Session = Depends(get_db)) -> Post:
    """Create new post"""
    if post.group_id:
        if not get_group(db, post.group_id):
            raise HTTPException(
                status_code=404,
                detail=f"Группа под номером: {post.group_id} не существует.")
    # Нужна проверка что переданный author_id есть в db
    return create_post(db, post)
