import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
class TestAdModel:
    def test_ad_creation(self, test_user):
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
    def test_proposal_creation(self, test_user, another_user, test_ad):
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
