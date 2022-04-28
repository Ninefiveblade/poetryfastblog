from typing import List, Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


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
