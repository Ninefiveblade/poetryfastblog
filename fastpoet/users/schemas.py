"""Schemas module for users"""
from typing import List, Optional

from pydantic import BaseModel

from fastpoet.posts.schemas import Post


class UserBase(BaseModel):
    id: int = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    username: Optional[str] = None
    posts: List[Post] = []


class UserCreate(UserBaseInDB):
    password: str


class UserInDB(UserBaseInDB):
    hashed_password: str


class User(UserBaseInDB):
    pass
