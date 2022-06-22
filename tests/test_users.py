"""Tests for users models, endpoints."""
from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.conftest import app

client = TestClient(app)


def test_users_enpoinds_active(test_db):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK, response.text


def test_create_user(test_db):
    response = client.post(
        "/auth/signup/", json={"username": "testname", "password": "test1234"}
    )
    assert response.status_code == HTTPStatus.CREATED, response.text
    assert response.json().get("username") == "testname"
    assert "id" in response.json()


def test_get_user(test_db):
    response = client.post(
        "/auth/signup/", json={"username": "testname", "password": "test1234"}
    )
    user_id = response.json().get("id")
    username = response.json().get("username")
    response = client.get(f"/users/{username}")
    assert response.status_code == HTTPStatus.OK, response.text
    assert response.json().get("username") == "testname"
    assert response.json().get("id") == user_id
    assert not response.json()["posts"]


def test_get_token(test_db):
    pass
