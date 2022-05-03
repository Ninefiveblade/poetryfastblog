"""Schemas module for users"""

from pydantic import BaseModel
from typing import List

from fastpoet.posts.schemas import Post


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True
