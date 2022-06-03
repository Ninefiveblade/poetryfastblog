"""Schemas module for posts"""
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    id: int = None
    author_id: Optional[int]

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    title: str
    text: str
    group_id: int = None


class PostList(PostCreate):
    pass
