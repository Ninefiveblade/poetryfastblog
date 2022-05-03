"""Schemas module for posts"""
from pydantic import BaseModel
from typing import Optional


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
