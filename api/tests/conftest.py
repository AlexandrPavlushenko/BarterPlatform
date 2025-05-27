import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APIClient

from ads.models import Ad, ExchangeProposal

User = get_user_model()

fake = Faker()


@pytest.fixture
def api_client():
    """Фикстура, предоставляющая экземпляр APIClient из Django REST Framework для тестирования API эндпоинтов."""
    return APIClient()


@pytest.fixture
def test_user(db):  # noqa
    """Фикстура создает и возвращает тестового пользователя с базовой информацией.

    Возвращает:
        User: Экземпляр пользователя Django с email 'test@example.com' и паролем 'testpass123'.
    """
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def another_user(db):  # noqa
    """Фикстура создает и возвращает второго тестового пользователя для сценариев, требующих нескольких пользователей.

    Возвращает:
        User: Экземпляр пользователя Django с email 'another@example.com' и паролем 'testpass123'.
    """
    return User.objects.create_user(
        email="another@example.com",
        password="testpass123",
        first_name="Another",
        last_name="User",
    )


@pytest.fixture
def test_ad(db, test_user):  # noqa
    """Фикстура создает и возвращает тестовое объявление, связанное с тестовым пользователем.

    Аргументы:
        test_user: Фикстура пользователя, который будет автором объявления.

    Возвращает:
        Ad: Экземпляр объявления с тестовыми данными, включая заголовок, описание, категорию и состояние.
    """
    ad = Ad.objects.create(
        author=test_user,
        title="Test Ad",
        description="Test Description",
        category="electronics",
        condition="new",
    )
    print(f"Created test ad: {ad.pk}")
    return ad


@pytest.fixture
def test_proposal(db, test_user, another_user, test_ad):  # noqa
    """Фикстура создает и возвращает тестовое предложение обмена между пользователями для тестового объявления.

    Аргументы:
        test_user: Пользователь, получающий предложение
        another_user: Пользователь, отправляющий предложение
        test_ad: Объявление, для которого создается предложение обмена

    Возвращает:
        ExchangeProposal: Экземпляр предложения обмена с тестовыми данными, включая комментарий.
    """
    return ExchangeProposal.objects.create(
        ad_sender=another_user,
        receiver_user=test_user,
        ad=test_ad,
        comment="Test proposal comment",
    )
