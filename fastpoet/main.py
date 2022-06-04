"""Приложение запуска app:main"""
from fastapi import FastAPI

from fastpoet.groups.routers import router as groups_router
from fastpoet.posts.routers import router as posts_router
from fastpoet.users.routers import (
    authentications_router,
    permissions_router,
    users_router
)


def create_app():
    """Application Initialization"""
    app = FastAPI()
    app.include_router(posts_router)
    app.include_router(users_router.router)
    app.include_router(permissions_router.router)
    app.include_router(authentications_router.router)
    app.include_router(groups_router)
    return app


app = create_app()
