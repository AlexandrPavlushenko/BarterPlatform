import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


@pytest.mark.django_db
class TestUserCreateView:
    def test_register_view_get(self, client):
        """Тест получения страницы регистрации пользователя.

        Args:
            client: Django test client.

        Asserts:
            - Страница регистрации успешно открывается (код 200).
            - В контексте ответа присутствует форма.
        """
        response = client.get(reverse("users:register"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_register_view_post(self, client):
        """Тест отправки формы регистрации.

        Args:
            client: Django test client.

        Asserts:
            - Форма успешно отправляется и происходит редирект (код 302).
            - Новый пользователь сохраняется в базе.
            - Отправляется письмо для активации аккаунта.
        """
        response = client.post(
            reverse("users:register"),
            {
                "email": "new@example.com",
                "password1": "complexpassword123",
                "password2": "complexpassword123",
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(email="new@example.com").exists()
        assert len(mail.outbox) == 1
        assert "Активируйте свой аккаунт" in mail.outbox[0].subject

    def test_register_invalid_data(self, client):
        """Тест регистрации с некорректными данными.

        Args:
            client: Django test client.

        Asserts:
            - Страница не редиректит и возвращает код 200.
            - В контексте ответа присутствует форма.
            - Пользователь с таким email не создаётся.
        """
        response = client.post(
            reverse("users:register"),
            {"email": "invalid", "password1": "123", "password2": "456"},
        )
        assert response.status_code == 200
        assert "form" in response.context
        assert not User.objects.filter(email="invalid").exists()


@pytest.mark.django_db
class TestActivateView:
    def test_activation_success(self, client):
        """Тест успешной активации пользователя по ссылке.

        Args:
            client: Django test client.

        Asserts:
            - После активации пользователь становится активным.
        """
        user = User.objects.create_user(
            email="activate@example.com", password="test123", is_active=False
        )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        response = client.get(
            reverse("users:activate", kwargs={"uidb64": uid, "token": token})
        )
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.is_active

    def test_activation_invalid_token(self, client):
        """Тест активации с некорректным токеном.

        Args:
            client: Django test client.

        Asserts:
            - После некорректной активации пользователь остаётся неактивным.
        """
        user = User.objects.create_user(
            email="activate2@example.com", password="test123", is_active=False
        )
        token = "invalid-token"
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        response = client.get(
            reverse("users:activate", kwargs={"uidb64": uid, "token": token})
        )
        assert response.status_code == 200
        user.refresh_from_db()
        assert not user.is_active


@pytest.mark.django_db
class TestUserProfileUpdateView:
    def test_profile_view_authenticated(self, client, test_user):
        """Тест получения страницы профиля авторизованным пользователем.

        Args:
            client: Django test client.
            test_user: Тестовый пользователь.

        Asserts:
            - Страница профиля успешно открывается (код 200).
            - В контексте присутствует форма.
        """
        client.force_login(test_user)
        response = client.get(reverse("users:profile"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_profile_update(self, client, test_user):
        """Тест обновления данных профиля пользователя.

        Args:
            client: Django test client.
            test_user: Тестовый пользователь.

        Asserts:
            - После отправки формы происходит редирект (код 302).
            - Данные пользователя обновляются.
        """
        client.force_login(test_user)
        response = client.post(
            reverse("users:profile"),
            {
                "first_name": "Updated",
                "last_name": "Name",
                "phone": "+1234567890",
                "city": "New York",
            },
        )
        assert response.status_code == 302
        test_user.refresh_from_db()
        assert test_user.first_name == "Updated"
        assert test_user.last_name == "Name"


@pytest.mark.django_db
class TestPasswordResetViews:
    def test_password_reset_request(self, client, test_user):
        """Тест запроса на сброс пароля пользователем.

        Args:
            client: Django test client.
            test_user: Тестовый пользователь.

        Asserts:
            - После запроса происходит редирект (код 302).
            - Отправляется письмо со ссылкой для сброса пароля.
        """
        response = client.post(
            reverse("users:password_reset"), {"email": test_user.email}
        )
        assert response.status_code == 302
        assert len(mail.outbox) == 1
        assert "Сброс пароля" in mail.outbox[0].subject

    def test_password_reset_confirm(self, client, test_user):
        """Тест подтверждения сброса пароля по ссылке.

        Args:
            client: Django test client.
            test_user: Тестовый пользователь.

        Asserts:
            - Страница подтверждения открывается (код 200).
            - После ввода нового пароля происходит редирект и пароль обновляется.
        """
        token = default_token_generator.make_token(test_user)
        uid = urlsafe_base64_encode(force_bytes(test_user.pk))

        # Получение страницы подтверждения
        response = client.get(
            reverse(
                "users:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
            )
        )
        assert response.status_code == 200

        # Отправка нового пароля
        response = client.post(
            reverse(
                "users:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
            ),
            {"password1": "newcomplexpass123", "password2": "newcomplexpass123"},
        )
        assert response.status_code == 302
        test_user.refresh_from_db()
        assert test_user.check_password("newcomplexpass123")
