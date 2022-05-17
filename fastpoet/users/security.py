from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .schemas import Token, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str):  # хешируем пароль
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password): # сверяем пароли
    return pwd_context.verify(plain_password, hashed_password)


