"""Routing module for users"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.settings import models, security_config
from fastpoet.settings.database import engine, get_db

from .schemas import Token, User, UserCreate, UserToken
from .security import oauth2_scheme
from .service import (add_user, authenticate_user, create_access_token,
                      get_user, get_user_by_username, get_users)

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.get("/users/", response_model=list[User])
def users_get(db: Session = Depends(get_db)):
    """Get users"""
    users = get_users(db)
    return users


@router.get("/users/{user_id}", response_model=User)
def user_get(user_id: int, db: Session = Depends(get_db)):
    """Get user by id"""
    user = get_user(db, user_id)
    return user


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create new user"""
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist",
        )
    return add_user(db=db, user=user)


@router.get("/test/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"auth": "если ты видишь это, то ты залогинен!"}


@router.post("/token/", response_model=Token)
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
