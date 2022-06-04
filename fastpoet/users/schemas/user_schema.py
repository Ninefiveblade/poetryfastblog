from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from fastpoet.posts.schemas import PostList


class UserBase(BaseModel):
    """Base user pydantic model."""
    id: int = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    """Expand UserBase, included posts set and username."""
    username: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    born_year: Optional[int]
    posts: List[PostList] = []


class UserCreate(UserBaseInDB):
    """Expand UserBaseInDB, included posts set and username and password."""
    username: str = Field(
        max_length=15,
        min_length=4,
        regex="[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$"
    )
    email: Optional[EmailStr]
    first_name: Optional[str] = Field(
        description="Введите имя киррилицей.",
        min_length=2,
        max_length=84,
        regex="[\u0401\u0451\u0410-\u044f]"
    )
    last_name: Optional[str] = Field(
        description="Введите фамилию киррилицей.",
        min_length=2,
        max_length=96,
        regex="[\u0401\u0451\u0410-\u044f]"
    )
    born_year: Optional[int] = None  # Добавить ограничения
    password: str = Field(
        min_length=8,
        regex="[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$"
    )

    @validator('username')
    def username_alphanumeric(cls, var):
        assert var.isalnum(), 'must be alphanumeric'
        return var

    @validator('password')
    def password_alphanumeric(cls, var):
        assert var.isalnum(), 'must be alphanumeric'
        return var


class UserInDB(UserBaseInDB):
    """
    Expand UserBaseInDB, included posts set and username and hashed_password.
    """
    hashed_password: str


class User(UserBaseInDB):
    """
    Expand UserBaseInDB, included posts set and username and password.
    Repeats UserBaseInDB and UserBase for understanding usage.
    """
    pass


class UserToken(UserBase):
    """
    POST token create form.
    Expands UserBase have a fields an id, username, pass.
    """
    username: str
    password: str
