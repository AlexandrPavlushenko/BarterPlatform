import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


@pytest.mark.django_db
class TestUserCreateView:
    def test_register_view_get(self, client):
        response = client.get(reverse("users:register"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_register_view_post(self, client):
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
        client.force_login(test_user)
        response = client.get(reverse("users:profile"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_profile_update(self, client, test_user):
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
        response = client.post(
            reverse("users:password_reset"), {"email": test_user.email}
        )
        assert response.status_code == 302
        assert len(mail.outbox) == 1
        assert "Сброс пароля" in mail.outbox[0].subject

    def test_password_reset_confirm(self, client, test_user):
        token = default_token_generator.make_token(test_user)
        uid = urlsafe_base64_encode(force_bytes(test_user.pk))

        # Get the confirm page
        response = client.get(
            reverse(
                "users:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
            )
        )
        assert response.status_code == 200

        # Post new password
        response = client.post(
            reverse(
                "users:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
            ),
            {"password1": "newcomplexpass123", "password2": "newcomplexpass123"},
        )
        assert response.status_code == 302
        test_user.refresh_from_db()
        assert test_user.check_password("newcomplexpass123")
