"""Schemas module for users"""
from typing import List, Optional, Union

from pydantic import BaseModel

from fastpoet.posts.schemas import PostList


class UserBase(BaseModel):
    """Base user pydantic model."""
    id: int = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    """Expand UserBase, included posts set
    and username.
    """
    username: Optional[str] = None
    posts: List[PostList] = []


class UserCreate(UserBaseInDB):
    """Expand UserBaseInDB, included posts set
    and username and password.
    """
    password: str


class UserInDB(UserBaseInDB):
    """Expand UserBaseInDB, included posts set
    and username and hashed_password."""
    hashed_password: str


class User(UserBaseInDB):
    """Expand UserBaseInDB, included posts set
    and username and password.
    repeats UserBaseInDB and UserBase
    for understanding usage."""
    pass


class UserToken(UserBase):
    """POST token create form.
    expands UserBase
    have a fields an id, username, pass."""
    username: str
    password: str


class Token(BaseModel):
    """Token form"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Create token data for current_user depends."""
    username: Union[str, None] = None
