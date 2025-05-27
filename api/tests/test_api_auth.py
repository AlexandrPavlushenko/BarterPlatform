import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestAuthAPI:
    """Тесты для API аутентификации и регистрации пользователей."""

    def test_user_registration(self, api_client):
        """Тест регистрации нового пользователя.

        Проверяет:
        - Успешное создание пользователя (код 201)
        - Наличие пользователя в базе данных после регистрации
        - Корректность переданных данных
        """
        url = reverse("api:user_register")
        data = {
            "email": "new@example.com",
            "password": "newpass123",
            "password2": "newpass123",
            "first_name": "New",
            "last_name": "User",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="new@example.com").exists()

    def test_token_obtain(self, api_client, test_user):
        """Тест получения JWT токена для аутентификации.

        Проверяет:
        - Успешное получение токенов (код 200)
        - Наличие access-токена в ответе
        - Наличие refresh-токена в ответе
        """
        url = reverse("api:token_obtain_pair")
        data = {"email": "test@example.com", "password": "testpass123"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
