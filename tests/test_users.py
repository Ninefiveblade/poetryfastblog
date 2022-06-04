"""Tests for users models, endpoints."""
from fastapi.testclient import TestClient

from tests.conftest import app

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
