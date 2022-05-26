from fastapi import status
from fastapi.testclient import TestClient

from .conftest import app

client = TestClient(app)


class TestUrlUserAPI:

    def test_get_users(self):
        """Получить список пользователей"""
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_by_id(self):
        """Получить пользователя по id"""
        response = client.get("/users/1/")
        assert response.status_code == status.HTTP_200_OK


class TestCreateUser:

    def test_user_post(self):
        """Создать нового пользователя"""
        response = client.post(
            "/users/",
            json={"username": "usertest", "password": "12345"},
        )
        assert response.status_code == status.HTTP_200_OK
