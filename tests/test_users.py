"""Tests for users models, endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastpoet.settings.database import Base, get_db
from fastpoet.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
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


def test_crud_user(test_db):
    response = client.post(
        "/auth/signup/",
        json={"username": "testname", "password": "test1234"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testname"
    assert "id" in data
    user_id = data["id"]
    username = data["username"]

    response = client.get(f"/users/{username}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testname"
    assert data["id"] == user_id
    assert not data["posts"]


def test_get_token(test_db):
    pass
