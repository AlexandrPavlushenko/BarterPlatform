import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APIClient

from ads.models import Ad, ExchangeProposal

User = get_user_model()

fake = Faker()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):  # noqa
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def another_user(db):  # noqa
    return User.objects.create_user(
        email="another@example.com",
        password="testpass123",
        first_name="Another",
        last_name="User",
    )


@pytest.fixture
def test_ad(db, test_user):  # noqa
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
    return ExchangeProposal.objects.create(
        ad_sender=another_user,
        receiver_user=test_user,
        ad=test_ad,
        comment="Test proposal comment",
    )
