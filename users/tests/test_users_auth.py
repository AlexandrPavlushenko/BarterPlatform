import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, client, test_user):
        """Тест успешного входа"""
        response = client.post(
            reverse("users:login"),
            {"username": test_user.email, "password": "testpass123"},
            follow=True,
        )
        assert response.status_code == 200
        assert response.context["user"].is_authenticated

    def test_login_failure(self, client, test_user):
        response = client.post(
            reverse("users:login"),
            {"username": test_user.email, "password": "wrongpassword"},
            follow=True,
        )

        # Проверяем наличие сообщения об ошибке
        messages = list(response.context["messages"])
        error_found = any(
            "Неверная почта или пароль" in str(m)
            or "Пожалуйста, введите правильные email и пароль" in str(m)
            for m in messages
        )
        assert error_found, "Сообщение об ошибке не найдено"

    def test_login_form_labels(self, client):
        """Проверка что форма использует email вместо username"""
        response = client.get(reverse("users:login"))
        form = response.context["form"]
        assert form.fields["username"].label == "Email"
        assert form.fields["password"].label == "Пароль"
