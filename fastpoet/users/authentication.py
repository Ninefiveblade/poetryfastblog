"""Authorization middleware."""
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from fastpoet.settings import security_config
from fastpoet.users.models import User


class BasicAuthBackend(AuthenticationBackend):
    """Аутентификация пользователя по токену.
    Если пользователь не аутентифицирован, присваиваем
    Unautorized User
    Если токен пользователя истек, выдаем ошибку.
    """
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                payload = jwt.decode(
                    credentials, security_config.SECRET_KEY,
                    algorithms=[security_config.ALGORITHM]
                )
                print(User(username=payload.get("sub")))
                return (
                    AuthCredentials(["authenticated"]),
                    User(username=payload.get("sub"))
                )
        except (ValueError, UnicodeDecodeError, ExpiredSignatureError):
            raise AuthenticationError(
                'Invalid basic auth credentials or token expired'
            )


middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]
