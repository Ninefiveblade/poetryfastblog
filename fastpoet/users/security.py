"""Secure depends for users."""
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .roles import Role  # импортируем роли для скупов в oauth2_scheme

#  pwd hash password by bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  check a token availability on user
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token/",
    scopes={  # роли из класса Role (roles.py)
        Role.GUEST["name"]: Role.GUEST["description"],
        Role.SUPER_USER["name"]: Role.SUPER_USER["description"],
        Role.USER["name"]: Role.USER["description"],
        Role.ADMIN["name"]: Role.ADMIN["description"],
        Role.MODERATOR["name"]: Role.MODERATOR["description"],
    },
)


def get_password_hash(password: str) -> str:
    """Create hashed user password."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Check plain password with hashed, return Bool."""
    return pwd_context.verify(plain_password, hashed_password)
