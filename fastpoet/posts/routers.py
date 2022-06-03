"""Routing module for posts."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.groups.service import get_group
from fastpoet.posts.models import Post
from fastpoet.settings.database import get_db
from fastpoet.users.service import get_user

from .schemas import PostCreate, PostList
from .service import create_post, get_posts

router = APIRouter()


@router.get(
    "/posts/", response_model=List[PostList], status_code=status.HTTP_200_OK
)
def posts_get(db: Session = Depends(get_db)) -> List[PostList]:
    """Get post list."""
    return get_posts(db)


@router.post(
    "/posts/", response_model=PostCreate, status_code=status.HTTP_201_CREATED
)
def post_create(post: PostCreate, db: Session = Depends(get_db)) -> Post:
    """Create new post."""
    if post.group_id:
        if not get_group(db, post.group_id):
            raise HTTPException(
                status_code=404,
                detail=f"Group number: {post.group_id} does not exist.")
    if not get_user(db, post.author_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Author number: {post.author_id} does not exist.",
        )
    return create_post(db, post)
