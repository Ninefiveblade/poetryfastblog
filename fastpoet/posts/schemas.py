"""Schemas module for posts"""
from pydantic import BaseModel


class PostBase(BaseModel):
    id: int = None

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    title: str
    text: str
    author_id: int
    group_id: int = None


class PostList(PostCreate):
    pass
