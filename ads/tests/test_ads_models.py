import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
class TestAdModel:
    """Тестирование модели объявления (Ad)."""

    def test_ad_creation(self, test_user):
        """Проверяет корректное создание объявления с базовыми полями.

        Args:
            test_user: Фикстура пользователя (автор объявления)

        Asserts:
            - Строковое представление соответствует заголовку
            - Автор объявления соответствует переданному пользователю
            - Категория сохраняется корректно
        """
        ad = Ad.objects.create(
            author=test_user,
            title="Test Ad",
            description="Test description",
            category="electronics",
            condition="new",
        )
        assert str(ad) == "Test Ad"
        assert ad.author == test_user
        assert ad.category == "electronics"

    def test_ad_image_upload(self, test_user):
        """Проверяет загрузку изображения для объявления.

        Args:
            test_user: Фикстура пользователя (автор объявления)

        Asserts:
            - Изображение сохраняется с правильным путем
        """
        image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        ad = Ad.objects.create(
            author=test_user,
            title="Ad with image",
            description="Test",
            category="clothing",
            condition="used",
            image=image,
        )
        assert "ads/images/test" in ad.image.name


@pytest.mark.django_db
class TestExchangeProposalModel:
    """Тестирование модели предложения обмена (ExchangeProposal)."""

    def test_proposal_creation(self, test_user, another_user, test_ad):
        """Проверяет создание предложения обмена с базовыми полями.

        Args:
            test_user: Фикстура пользователя (отправитель предложения)
            another_user: Фикстура пользователя (получатель предложения)
            test_ad: Фикстура тестового объявления

        Asserts:
            - Статус по умолчанию 'pending'
            - Строковое представление содержит информацию об участниках и объявлении
        """
        proposal = ExchangeProposal.objects.create(
            ad_sender=test_user,
            receiver_user=another_user,
            ad=test_ad,
            comment="Test proposal",
        )
        assert proposal.status == "pending"
        assert (
            str(proposal)
            == f"Предложение от {test_user} к {another_user} для объявления '{test_ad.title}'"
        )

    def test_unique_together_constraint(self, test_user, test_ad):
        """Проверяет ограничение уникальности для предложений обмена.

        Args:
            test_user: Фикстура пользователя (отправитель предложения)
            test_ad: Фикстура тестового объявления

        Asserts:
            - При попытке создать дублирующее предложение вызывается IntegrityError
        """
        ExchangeProposal.objects.create(
            ad_sender=test_user,
            receiver_user=test_ad.author,
            ad=test_ad,
            comment="First proposal",
        )
        with pytest.raises(IntegrityError):
            ExchangeProposal.objects.create(
                ad_sender=test_user,
                receiver_user=test_ad.author,
                ad=test_ad,
                comment="Duplicate proposal",
            )
