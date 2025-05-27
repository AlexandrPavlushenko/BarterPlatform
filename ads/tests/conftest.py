from io import BytesIO

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from ads.models import Ad, ExchangeProposal

User = get_user_model()


@pytest.fixture
def test_ad(db, test_user):
    """Фикстура создает тестовое объявление для использования в тестах.

    Args:
        db: Фикстура доступа к тестовой базе данных
        test_user: Фикстура пользователя (автор объявления)

    Returns:
        Ad: Созданный объект объявления с базовыми тестовыми данными
    """
    return Ad.objects.create(
        author=test_user,
        title="Test Ad",
        description="Test description",
        category="electronics",
        condition="new",
    )


@pytest.fixture
def test_proposal(db, test_user, another_user, test_ad):
    """Фикстура создает тестовое предложение обмена между пользователями.

    Args:
        db: Фикстура доступа к тестовой базе данных
        test_user: Фикстура пользователя (получатель предложения)
        another_user: Фикстура пользователя (отправитель предложения)
        test_ad: Фикстура объявления, к которому относится предложение

    Returns:
        ExchangeProposal: Созданный объект предложения обмена с тестовыми данными
    """
    return ExchangeProposal.objects.create(
        ad_sender=another_user,
        receiver_user=test_user,
        ad=test_ad,
        comment="Test proposal",
    )


def ad_image():
    """Создает валидное тестовое изображение в формате JPEG для тестирования загрузки.

    Returns:
        SimpleUploadedFile: Файл изображения в формате JPEG (100x100 пикселей, красный цвет),
        готовый для использования в тестах загрузки файлов
    """
    # Создаем красное изображение 100x100 пикселей
    image = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95)

    return SimpleUploadedFile(
        name="test.jpg", content=buffer.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def test_user(db):
    """Фикстура создает основного тестового пользователя.

    Args:
        db: Фикстура доступа к тестовой базе данных

    Returns:
        User: Объект пользователя с тестовыми данными:
        - email: test@example.com
        - password: testpass123
        - Имя: Test
        - Фамилия: User
    """
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def another_user(db):
    """Фикстура создает дополнительного тестового пользователя.

    Args:
        db: Фикстура доступа к тестовой базе данных

    Returns:
        User: Объект пользователя с тестовыми данными:
        - email: another@example.com
        - password: testpass123
        - Имя: Another
        - Фамилия: User
    """
    return User.objects.create_user(
        email="another@example.com",
        password="testpass123",
        first_name="Another",
        last_name="User",
    )
