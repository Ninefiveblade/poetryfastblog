"""Routing module for users."""
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from fastpoet.settings.database import get_db

from fastpoet.users.schemas.user_schema import User
from fastpoet.users.security import oauth2_scheme
from fastpoet.users.crud import crud_user
from fastpoet.users.security import get_current_user
from fastpoet.users.decorators import is_user_admin

router = APIRouter()


@router.get("/users/", response_model=List[User])
def users_get(db: Session = Depends(get_db)) -> List[User]:
    """Get users."""
    return crud_user.get_users(db)


@router.get("/users/{username}", response_model=User)
def user_get_by_username(username: str, db: Session = Depends(get_db)) -> User:
    """Get user by username."""
    user = crud_user.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    return user


@router.patch("/users/{username}", response_model=User)
@is_user_admin
def user_patch_by_username(
    edit_user: User,
    username: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get user by username."""
    user = crud_user.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    if crud_user.get_user_by_username(db, edit_user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    return crud_user.update_user(db, user, edit_user)


@router.delete("/users/{username}")
@is_user_admin
def delete_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = crud_user.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    crud_user.destroy_user_by_username(db, user.username)
    return {"info": f"{user.username} has been deleted."}


@router.get("/users/me/", response_model=User, status_code=status.HTTP_200_OK)
def get_detail_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Get detail user."""
    user: User = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    return user


@router.patch(
    "/users/me/", response_model=User, status_code=status.HTTP_201_CREATED,
)
def user_patch(
    edit_user: User,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Update detail user."""
    current_user: User = get_current_user(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    return crud_user.update_user(db, current_user, edit_user)


@router.delete("/users/me/", status_code=status.HTTP_200_OK)
def user_destroy(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Dict:
    """Delete user."""
    current_user: User = get_current_user(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    crud_user.destroy_user_by_username(db, current_user.username)
    return {"info": f"{current_user.username} has been deleted."}


@router.get("/some/")
def test_get(request: Request):
    print(request.user.email)
    return {"info": "username"}
