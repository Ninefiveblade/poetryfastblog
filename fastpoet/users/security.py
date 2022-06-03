"""Secure depends for users."""
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token/",
)


def get_password_hash(password: str) -> str:
    """Create hashed user password."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Check plain password with hashed, return Bool."""
    return pwd_context.verify(plain_password, hashed_password)
