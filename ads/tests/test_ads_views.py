import pytest
from django.urls import reverse

from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
class TestAdViews:
    def test_ad_list_view(self, client, test_ad):
        response = client.get(reverse("ads:ad_list"))
        assert response.status_code == 200
        assert test_ad.title.encode() in response.content

    def test_ad_detail_view(self, client, test_ad):
        response = client.get(reverse("ads:ad_detail", kwargs={"pk": test_ad.pk}))
        assert response.status_code == 200
        assert test_ad.title.encode() in response.content

    def test_ad_create_view(self, client, test_user):
        client.force_login(test_user)
        response = client.post(
            reverse("ads:ad_create"),
            {
                "title": "New Ad",
                "description": "New description",
                "category": "electronics",
                "condition": "new",
            },
        )
        assert response.status_code == 302
        assert Ad.objects.filter(title="New Ad").exists()


@pytest.mark.django_db
class TestExchangeProposalViews:
    def test_proposal_create_view(self, client, test_user, test_ad):
        client.force_login(test_user)
        response = client.post(
            reverse("ads:exchange_create", kwargs={"ad_id": test_ad.pk}),
            {"comment": "Test proposal"},
        )
        assert response.status_code == 302  # Проверяем редирект
        assert ExchangeProposal.objects.filter(ad=test_ad, ad_sender=test_user).exists()

    def test_accept_proposal_view(self, client, test_user, test_proposal):
        client.force_login(test_user)
        response = client.post(
            reverse("ads:accept_proposal", kwargs={"pk": test_proposal.pk})
        )
        test_proposal.refresh_from_db()
        assert test_proposal.status == "accepted"
