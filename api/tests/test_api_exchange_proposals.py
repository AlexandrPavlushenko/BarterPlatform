import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import ExchangeProposal


@pytest.mark.django_db
class TestExchangeProposalAPI:
    def test_proposal_create(self, api_client, another_user, test_ad):
        api_client.force_authenticate(user=another_user)
        url = reverse("api:exchange_proposal_create")
        data = {"ad": test_ad.pk, "comment": "Test proposal comment"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert ExchangeProposal.objects.filter(ad=test_ad).exists()

    def test_proposal_create_to_own_ad(self, api_client, test_user, test_ad):
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_create")
        response = api_client.post(url, {"ad": test_ad.pk})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_proposal_list_authenticated(self, api_client, test_user, test_proposal):
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_proposal_detail_owner(self, api_client, test_user, test_proposal):
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_detail", kwargs={"pk": test_proposal.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "Test proposal comment"

    def test_proposal_update_status(self, api_client, test_user, test_proposal):
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_update", kwargs={"pk": test_proposal.pk})
        data = {"status": "accepted"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        test_proposal.refresh_from_db()
        assert test_proposal.status == "accepted"

    def test_proposal_delete_sender(self, api_client, another_user, test_proposal):
        api_client.force_authenticate(user=another_user)
        url = reverse("api:exchange_proposal_delete", kwargs={"pk": test_proposal.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ExchangeProposal.objects.filter(pk=test_proposal.pk).exists()
