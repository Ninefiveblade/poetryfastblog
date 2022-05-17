"""Routing module for users"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from fastpoet.settings.database import engine
from .schemas import User, UserCreate, UserToken, Token
from .service import (
    add_user,
    get_user,
    get_users,
    get_user_by_username,
    authenticate_user,
    create_access_token
)
from fastpoet.settings import security_config
from fastpoet.settings.database import get_db
from fastpoet.settings import models

router = APIRouter()

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


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

# пока постоянно можно выдавать токен
# хоть каждый раз
# потом сделаем проверку на это, пока посмотри.
# все токены активны, даже если пересоздавать
@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # добавить обработку исключений, если юзер есть в базе
    # если юзер уже есть с таким ником
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


@router.post("/token", response_model=Token)
def login(form_data: UserToken, db: Session = Depends(get_db)):
    """Сама форма получения токена."""
    user = get_user_by_username(db, form_data.username) # вот тут проверяем, что такой юзер уже есть
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found user with this username",
        )
    auth = authenticate_user(db, form_data.username, form_data.password) # вот тут авторизируем пользователя
    if not auth: # если метча нет, даем ошибку
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES) # устанавливаем время житья токена
    access_token = create_access_token( # создаем токен 
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"} # отправляем юзеру
