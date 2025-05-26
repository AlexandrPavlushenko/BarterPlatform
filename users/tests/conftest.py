import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

User = get_user_model()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
        phone="+1234567890",
        city="Test City",
    )


@pytest.fixture
def test_superuser(db):
    return User.objects.create_superuser(
        email="admin@example.com", password="adminpass123"
    )


@pytest.fixture
def avatar_file():
    """Фикстура создает валидный JPEG-файл"""
    from PIL import Image
    from io import BytesIO

    # Создаем красное изображение 100x100
    image = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")

    return SimpleUploadedFile(
        name="test_avatar.jpg", content=buffer.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def client():
    """Фикстура для тестового клиента"""
    return Client()


@pytest.fixture
def test_user(db):
    """Фикстура для тестового пользователя"""
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )
