"""Schemas module for users."""
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, validator

from fastpoet.posts.schemas import PostList


class RoleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        orm_mode = True


class Role(RoleInDBBase):
    pass


class RoleInDB(RoleInDBBase):
    pass


class UserRoleBase(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    role_id: int


class UserRoleInDBBase(UserRoleBase):
    role: Role

    class Config:
        orm_mode = True


class UserRole(UserRoleInDBBase):
    pass


class UserRoleInDB(UserRoleInDBBase):
    pass


class UserBase(BaseModel):
    """Base user pydantic model."""
    id: int = None

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    """Expand UserBase, included posts set and username."""
    username: str = Field(
        max_length=15,
        min_length=4,
        regex="[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$"
    )
    first_name: Optional[str]
    last_name: Optional[str]
    born_year: Optional[int]
    user_role: Optional[UserRole]
    posts: List[PostList] = []


class UserCreate(UserBaseInDB):
    """Expand UserBaseInDB, included posts set and username and password."""
    email: Optional[EmailStr] = None
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
    #  user_role: Optional[UserRole]

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


class Token(BaseModel):
    """Token form"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Create token data for current_user depends."""
    username: Union[str, None] = None
    scopes: List[str] = []


#  Схемы ролей и юзерролей
