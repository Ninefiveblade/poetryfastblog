from pydantic import BaseModel


class PostBase(BaseModel):
    title: str


class PostCreate(PostBase):
    test: str
