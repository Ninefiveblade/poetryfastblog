from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.settings import security_config
from fastpoet.settings.database import get_db
from fastpoet.users.crud.crud_authentication import (authenticate_user,
                                                     create_access_token)
from fastpoet.users.crud.crud_user import add_user, get_user_by_username
from fastpoet.users.schemas import token_schema, user_schema

router = APIRouter()


@router.post(
    "/auth/signup/",
    response_model=user_schema.User,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: user_schema.UserCreate, db: Session = Depends(get_db)
) -> user_schema.User:
    """Create new user."""
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с именем '{user.username}' уже существует.",
        )
    return add_user(db, user)


@router.post(
    "/auth/token/",
    response_model=token_schema.Token,
    status_code=status.HTTP_201_CREATED
)
def get_token_for_user(
    form_data: user_schema.UserToken, db: Session = Depends(get_db)
) -> Dict:
    """Get token."""
    user: user_schema.User = get_user_by_username(db, form_data.username)
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
