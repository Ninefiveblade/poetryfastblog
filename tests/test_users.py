"""Tests for users models, endpoints."""
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastpoet.main import app
from fastpoet.settings.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_users_enpoinds_active(test_db):
    response = client.get("/users/")
    assert response.status_code == 200, response.text


def test_crud_user(test_db):
    response = client.post(
        "/auth/signup/", json={"username": "testname", "password": "test1234"}
    )
    assert response.status_code == 201, response.text
    assert response.json()["username"] == "testname"
    assert "id" in response.json()
    user_id = response.json()["id"]
    username = response.json()["username"]

    response = client.get(f"/users/{username}")
    assert response.status_code == 200, response.text
    assert response.json()["username"] == "testname"
    assert response.json()["id"] == user_id
    assert not response.json()["posts"]


def test_get_token(test_db):
    pass
