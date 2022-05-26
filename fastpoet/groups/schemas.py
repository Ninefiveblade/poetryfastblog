"""Schemas module for groups."""
from pydantic import BaseModel


class GroupBase(BaseModel):
    id: int = None

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    title: str
    slug: str
    description: str = None


class GroupList(GroupCreate):
    pass
