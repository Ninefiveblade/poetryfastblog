from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
import base64
import binascii

from fastpoet.users.models import User


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            # переносы от бога
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")  # разобрать код
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")  # разобрать код
        # TODO: осуществить проверку имени и пароля
        return AuthCredentials(["authenticated"]), User(username)


middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]
