import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from ads.models import Ad, ExchangeProposal
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO

User = get_user_model()


@pytest.fixture
def test_ad(db, test_user):
    return Ad.objects.create(
        author=test_user,
        title="Test Ad",
        description="Test description",
        category="electronics",
        condition="new",
    )


@pytest.fixture
def test_proposal(db, test_user, another_user, test_ad):
    return ExchangeProposal.objects.create(
        ad_sender=another_user,
        receiver_user=test_user,
        ad=test_ad,
        comment="Test proposal",
    )


def ad_image():
    """Фикстура создает валидное тестовое изображение в формате JPEG"""
    # Создаем красное изображение 100x100 пикселей
    image = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95)

    return SimpleUploadedFile(
        name="test.jpg", content=buffer.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def test_user(db):
    """Фикстура для тестового пользователя"""
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def another_user(db):
    """Фикстура для второго пользователя"""
    return User.objects.create_user(
        email="another@example.com",
        password="testpass123",
        first_name="Another",
        last_name="User",
    )
