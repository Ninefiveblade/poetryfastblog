"""Routing module for users"""
from datetime import timedelta
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.settings import security_config
from fastpoet.settings.database import get_db

from .schemas import Token, User, UserCreate, UserToken
from .security import oauth2_scheme
from .service import (add_user, authenticate_user, create_access_token,
                      destroy_user_by_username, get_user_by_username,
                      get_users, update_user)

router = APIRouter()


@router.get("/users/", response_model=List[User])
def users_get(db: Session = Depends(get_db)) -> List[User]:
    """Get users"""
    return get_users(db)


@router.get("/users/{username}", response_model=User)
def user_get(username: str, db: Session = Depends(get_db)) -> User:
    """Get user by username"""
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    return user


@router.patch(
    "/users/{username}",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
def user_patch(
    username: str,
    edit_user: User,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Update detail user."""
    current_user: User = get_user_by_username(db, username)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    return update_user(db, current_user, edit_user)


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def user_destroy(
    username: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> Dict:
    """Delete user by username."""
    if not get_user_by_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist",
        )
    destroy_user_by_username(db, username)
    return {"info": f"User with username: {username} has been deleted."}


@router.post(
    "/auth/signup/", response_model=User, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create new user."""
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с именем `{user.username}` уже существует.",
        )
    return add_user(db, user)


@router.post(
    "/auth/token/", response_model=Token, status_code=status.HTTP_201_CREATED
)
def get_token_for_user(
    form_data: UserToken,
    db: Session = Depends(get_db)
) -> Dict:
    """Получение токена"""
    user: User = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found user with this username",
        )
    auth = authenticate_user(db, form_data.username, form_data.password)
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Время жизни токена
    access_token_expires = timedelta(
        minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Создание токена
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
