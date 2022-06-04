from typing import Optional

from pydantic import BaseModel


class Permissions(BaseModel):
    """Set perm. for Users."""
    username: str
    is_admin: Optional[bool]
    is_user: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
