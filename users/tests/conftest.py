import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

User = get_user_model()


@pytest.fixture
def test_user(db):
    """
    Создает и возвращает тестового пользователя.

    Returns:
        User: Созданный пользователь с заданными данными.
    """
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
    """
    Создает и возвращает тестового суперпользователя.

    Returns:
        User: Созданный суперпользователь с заданными данными.
    """
    return User.objects.create_superuser(
        email="admin@example.com", password="adminpass123"
    )


@pytest.fixture
def avatar_file():
    """
    Создаёт валидный JPEG-файл изображения для использования в тестах.

    Returns:
        SimpleUploadedFile: Объект, представляющий JPEG-файл изображения.
    """
    from io import BytesIO

    from PIL import Image

    # Создаем красное изображение 100x100
    image = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")

    return SimpleUploadedFile(
        name="test_avatar.jpg", content=buffer.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def client():
    """
    Создаёт тестовый клиент Django для выполнения HTTP-запросов в тестах.

    Returns:
        Client: Экземпляр тестового клиента Django.
    """
    return Client()
