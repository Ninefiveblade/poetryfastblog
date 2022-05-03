"""Тестирование"""
from fastapi import FastAPI

from fastpoet.posts.routers import router as posts_router
from fastpoet.users.routers import router as users_router


def create_app():
    """Application Initialization"""
    app = FastAPI()
    app.include_router(posts_router)
    app.include_router(users_router)
    return app


app = create_app()
