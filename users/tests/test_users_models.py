import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        """Тест создания пользователя с базовыми параметрами.

        Args:
            None

        Asserts:
            Email пользователя совпадает с указанным.
            Пароль пользователя установлен и корректно хеширован.
            По умолчанию пользователь не является staff и superuser.
            Пользователь активен.
        """
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active

    def test_create_superuser(self):
        """Тест создания суперпользователя.

        Args:
            None

        Asserts:
            Суперпользователь является staff и superuser.
            Суперпользователь активен.
        """
        admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        assert admin.is_staff
        assert admin.is_superuser
        assert admin.is_active

    def test_email_unique(self):
        """Тест уникальности email.

        Args:
            None

        Asserts:
            При попытке создать пользователя с уже существующим email выбрасывается IntegrityError.
        """
        User.objects.create_user(email="test@example.com", password="testpass123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(email="test@example.com", password="anotherpass")

    def test_optional_fields(self):
        """Тест заполнения необязательных полей.

        Args:
            None

        Asserts:
            Все необязательные поля корректно устанавливаются при создании пользователя.
        """
        user = User.objects.create_user(
            email="optional@example.com",
            password="test123",
            first_name="John",
            last_name="Doe",
            phone="+1234567890",
            city="New York",
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.phone == "+1234567890"
        assert user.city == "New York"

    def test_avatar_upload(self):
        """Тест загрузки файла-аватара.

        Args:
            None

        Asserts:
            Файл аватара корректно сохранён в поле avatar пользователя.
        """
        avatar = SimpleUploadedFile(
            "avatar.jpg", b"file_content", content_type="image/jpeg"
        )
        user = User.objects.create_user(
            email="avatar@example.com", password="test123", avatar=avatar
        )
        assert "avatars/avatar" in user.avatar.name

    def test_str_representation(self):
        """Тест строкового представления пользователя.

        Args:
            None

        Asserts:
            Метод __str__ возвращает email пользователя.
        """
        user = User.objects.create_user(email="str@example.com", password="test123")
        assert str(user) == "str@example.com"
