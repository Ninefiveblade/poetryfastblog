"""Dependensies and CRUD for users."""
from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from fastpoet.users import security
from fastpoet.users.models import User
from fastpoet.users.schemas.user_schema import UserCreate


def add_user(db: Session, user: UserCreate) -> User:
    """Add new user to db."""
    db_user = User(
        username=user.username,
        hashed_password=security.get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    """Grab user from db by id."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Grab user from db by username."""
    return db.query(User).filter(User.username == username).first()


def destroy_user_by_username(db: Session, username: str):
    """Delete user."""
    db.query(User).filter(User.username == username).delete()
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get users set."""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(
    db: Session,
    current_user: User,
    edit_user: Union[User, Dict[str, Any]],
) -> User:
    if isinstance(edit_user, dict):
        update_data = edit_user
    else:
        update_data = edit_user.dict(exclude_unset=True)
    if "password" in update_data:
        hashed_password: str = security.get_password_hash(
            update_data["password"]
        )
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
