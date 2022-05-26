"""Schemas module for posts"""
from typing import List

from pydantic import BaseModel

from ..groups.schemas import GroupList


class PostBase(BaseModel):
    id: int = None

    class Config:
        orm_mode = True


# class PostBaseInDB(PostBase):
#     group: List[GroupList] = []


class PostCreate(PostBase):
    title: str
    text: str
    author_id: int
    group_id: int = None


class PostList(PostCreate):
    pass
