"""Token schemas for users module."""
from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    """Token form"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Create token data for current_user depends."""
    username: Union[str, None] = None
