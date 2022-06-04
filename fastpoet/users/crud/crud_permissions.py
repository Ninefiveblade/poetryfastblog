"""Dependensies and CRUD for users."""
from typing import Dict, Union

from sqlalchemy.orm import Session

from fastpoet.users.models import User


def update_permission(
    db: Session,
    user: User,
    edit_user: Union[User, Dict[str, bool]],
) -> User:
    if isinstance(user, dict):
        update_data = edit_user
    else:
        update_data = edit_user.dict()
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
