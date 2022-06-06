"""Routing module for posts."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.groups.service import get_group
from fastpoet.posts.crud import crud_post
from fastpoet.posts.models import Post
from fastpoet.settings.database import get_db
from fastpoet.users.schemas.user_schema import User
from fastpoet.users.security import get_current_user, oauth2_scheme

from .schemas import PostCreate, PostList

router = APIRouter()


@router.get(
    "/posts/", response_model=List[PostList], status_code=status.HTTP_200_OK
)
def posts_get(db: Session = Depends(get_db)) -> List[PostList]:
    """Get post list."""
    return crud_post.get_posts(db)


@router.post(
    "/posts/", response_model=PostCreate, status_code=status.HTTP_201_CREATED
)
def post_create(
    post: PostCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Post:
    """Create new post."""
    user: User = get_current_user(db, token)
    post.author_id = user.id
    if post.group_id:
        if not get_group(db, post.group_id):
            raise HTTPException(
                status_code=404,
                detail=f"Group number: {post.group_id} does not exist.")
    return crud_post.create_post(db, post)
