"""Tests for users models, endpoints."""
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.conftest import app

client = TestClient(app)


@pytest.fixture
def user_fixture():
    response = client.post(
        "/auth/signup/", json={"username": "testname", "password": "test1234"}
    )
    return response


def test_users_enpoinds_active(test_db):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK, response.text
    assert isinstance(response.json(), list)


def test_create_user(test_db, user_fixture):
    assert user_fixture.status_code == HTTPStatus.CREATED, user_fixture.text
    assert user_fixture.json().get("username") == "testname"
    assert "id" in user_fixture.json()


def test_get_user_by_username(test_db, user_fixture):
    user_id = user_fixture.json().get("id")
    username = user_fixture.json().get("username")
    response = client.get(f"/users/{username}")
    assert response.status_code == HTTPStatus.OK, response.text
    assert response.json().get("username") == username
    assert response.json().get("id") == user_id
    assert not response.json().get("posts")


def test_delete_user_by_username(test_db, user_fixture):
    username = user_fixture.json().get("username")
    response = client.delete(f"/users/{username}")
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
    assert response.json().get("username") != username


def test_get_token(test_db):
    pass
