from fastapi import status
from fastapi.testclient import TestClient

from fastpoet.main import app

client = TestClient(app)


class TestUrlUserAPI:

    def test_get_users(self):
        """Получить список пользователей"""
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_by_id(self):
        "Получить пользователя по id"
        response = client.get("/users/1/")
        assert response.status_code == status.HTTP_200_OK
