"""Decorators for users."""
from functools import wraps

from fastapi import HTTPException, status

from fastpoet.users.security import get_current_user


def is_user_admin(func):
    """Decorator func. for check permissions."""
    @wraps(func)
    def wrapper(**kwargs):
        user = get_current_user(kwargs.get("db"), kwargs.get("token"))
        if not (user.is_admin or user.is_superuser):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission have only admin or superuser.",
                )
        return func(**kwargs)
    return wrapper
