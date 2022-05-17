"""Routing module for users"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastpoet.settings.database import engine
from .schemas import User, UserCreate, UserInDB
from .service import add_user, get_user, get_users, get_user_by_username
from .security import get_password_hash
from fastpoet.settings.database import get_db
from fastpoet.settings import models

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
    return add_user(db=db, user=user)


@router.get("/test/")
def get_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return {"token": token}


@router.post("/token")
#  доделать
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_username(db, form_data.username)
    print(user)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    user = UserInDB(**user.__dict__)
    hashed_password = get_password_hash(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}
