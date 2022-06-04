"""Routing module for users."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastpoet.settings.database import get_db
from fastpoet.users.schemas.permission_schema import Permissions
from fastpoet.users.schemas.user_schema import User
from fastpoet.users.crud.crud_user import get_user_by_username
from fastpoet.users.crud.crud_permissions import update_permission
from fastpoet.users.security import oauth2_scheme
from fastpoet.users.decorators import is_user_admin

router = APIRouter()


@router.patch("/user/permissions/", response_model=Permissions)
@is_user_admin
def set_permission(
    set_perm: Permissions,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user: User = get_user_by_username(db, set_perm.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found user with this username",
        )
    return update_permission(db, user, set_perm)
