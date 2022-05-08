"""Schemas module for users"""
from typing import List, Optional

from pydantic import BaseModel

from fastpoet.posts.schemas import Post


class UserBase(BaseModel):
    username: Optional[str] = None


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserCreate(UserBaseInDB):
    password: str


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str