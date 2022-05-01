"""Тестирование"""
from fastapi import FastAPI

from fastpoet.routers import router


def create_app():
    """Application Initialization"""
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()
