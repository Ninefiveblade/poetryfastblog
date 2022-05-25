"""Тестирование"""
from typing import Tuple, List

from fastapi_auth_middleware import FastAPIUser
from starlette.authentication import BaseUser
from fastapi import FastAPI, Depends
from fastapi_auth_middleware import AuthMiddleware
from sqlalchemy.orm import Session

from fastpoet.settings import security_config
from fastpoet.settings.database import get_db
from fastpoet.users.service import get_current_user
from fastpoet.posts.routers import router as posts_router
from fastpoet.users.routers import router as users_router

def create_app():
    """Application Initialization"""
    app = FastAPI()
    app.include_router(posts_router)
    app.include_router(users_router)
    return app

def verify_authorization_header(
    auth_header: str,
    db: Session = Depends(get_db)
) -> Tuple[List[str], BaseUser]: # Returns a Tuple of a List of scopes (string) and a BaseUser
    user = FastAPIUser(first_name="Anonymous", last_name="User", user_id=1)
    scopes = []
    if auth_header.get('authorization'):
        True
    print()
    return scopes, user

app = create_app()
app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)