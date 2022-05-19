from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


def get_password_hash(password: str) -> str:
    """Функция принимает пароль и возвращает хеш пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Функция сверяет пароль с хеш паролем, возвращает True или False"""
    return pwd_context.verify(plain_password, hashed_password)
