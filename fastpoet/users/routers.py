"""Routing module for users"""
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from fastpoet.settings import security_config
from fastpoet.settings.database import engine, get_db
from .models import User as user_model
from .schemas import Token, User, UserCreate, UserToken
from .security import oauth2_scheme
from .service import (add_user, authenticate_user, create_access_token,
                      get_current_user, get_user_by_username, get_users)

router = APIRouter()

user_model.metadata.create_all(bind=engine)


@router.get("/users/", response_model=List[User])
def users_get(db: Session = Depends(get_db)) -> List[User]:
    """Get users"""
    return get_users(db)


@router.get("/users/{username}", response_model=User)
def user_get(username: str, db: Session = Depends(get_db)) -> User:
    """Get user by username"""
    return get_user_by_username(db, username)


@router.post("/auth/signup/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create new user."""
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist",
        )
    return add_user(db, user)


@router.post("/auth/token/", response_model=Token)
def get_token_for_user(form_data: UserToken, db: Session = Depends(get_db)):
    """Получение токена"""
    user = get_user_by_username(db, form_data.username)
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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/items/{item_id}")
def read_root(item_id: str, request: Request,
              token: str = Depends(oauth2_scheme),
              db: Session = Depends(get_db)):
    print(token)
    get_current_user(db, token)
    client_host = request.user
    print(client_host)
    return {"client_host": client_host, "item_id": item_id}
