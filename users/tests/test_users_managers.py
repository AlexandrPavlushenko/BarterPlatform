import pytest
from django.contrib.auth import get_user_model

from users.managers import CustomUserManager

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserManager:
    def test_create_user(self):
        """
        Тестирует создание обычного пользователя с корректными email и паролем.

        Asserts:
            Email пользователя совпадает с ожидаемым и пароль установлен верно.
        """
        manager = CustomUserManager()
        manager.model = User

        user = manager.create_user(
            email="manager@example.com", password="managerpass123"
        )
        assert user.email == "manager@example.com"
        assert user.check_password("managerpass123")

    def test_create_user_no_email(self):
        """
        Тестирует, что при отсутствии email вызывается ValueError.

        Asserts:
            При попытке создания пользователя без email возникает ValueError с ожидаемым сообщением.
        """
        manager = CustomUserManager()
        manager.model = User

        with pytest.raises(
            ValueError, match="Пользователю необходимо указать адрес электронной почты"
        ):
            manager.create_user(email="", password="test123")

    def test_create_superuser(self):
        """
        Тестирует создание суперпользователя через менеджер.

        Asserts:
            Суперпользователь имеет is_staff и is_superuser, равные True.
        """
        manager = CustomUserManager()
        manager.model = User

        admin = manager.create_superuser(
            email="super@example.com", password="superpass123"
        )
        assert admin.is_staff
        assert admin.is_superuser

    def test_create_superuser_not_staff(self):
        """
        Тестирует невозможность создания суперпользователя с is_staff=False.

        Asserts:
            Создание суперпользователя с is_staff=False вызывает ValueError с ожидаемым текстом.
        """
        manager = CustomUserManager()
        manager.model = User

        with pytest.raises(
            ValueError, match="Суперпользователь должен иметь is_staff=True."
        ):
            manager.create_superuser(
                email="super2@example.com", password="superpass123", is_staff=False
            )

    def test_create_superuser_not_superuser(self):
        """
        Тестирует невозможность создания суперпользователя с is_superuser=False.

        Asserts:
            Создание суперпользователя с is_superuser=False вызывает ValueError с ожидаемым текстом.
        """
        manager = CustomUserManager()
        manager.model = User

        with pytest.raises(
            ValueError, match="Суперпользователь должен иметь is_superuser=True."
        ):
            manager.create_superuser(
                email="super3@example.com", password="superpass123", is_superuser=False
            )
