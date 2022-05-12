"""Routing module for users"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastpoet.settings import models
from fastpoet.settings.database import SessionLocal, engine

from .schemas import User, UserCreate
from .service import add_user, get_user, get_users
from .security import (
    get_password_hash, UserInDB, get_current_active_user
)

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    return add_user(db=db, user=user)


@router.get("/test/")
def get_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return {"token": token}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = get_db().get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = get_password_hash(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
