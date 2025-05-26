import pytest
from django.urls import reverse
from rest_framework import status
from ads.models import Ad


@pytest.mark.django_db
class TestAdAPI:
    def test_ad_list(self, api_client, test_ad):
        url = reverse("api:ad_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "Test Ad"

    def test_ad_create_authenticated(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = reverse("api:ad_create")
        data = {
            "title": "New Ad",
            "description": "New Description",
            "category": "clothing",
            "condition": "used",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Ad.objects.filter(title="New Ad").exists()

    def test_ad_create_unauthenticated(self, api_client):
        url = reverse("api:ad_create")
        response = api_client.post(url, {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_ad_detail(self, api_client, test_ad):
        url = reverse("api:ad_detail", kwargs={"pk": test_ad.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Ad"

    def test_ad_update_owner(self, api_client, test_user, test_ad):
        api_client.force_authenticate(user=test_user)
        url = reverse("api:ad_update", kwargs={"pk": test_ad.pk})
        data = {"title": "Updated Title"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        test_ad.refresh_from_db()
        assert test_ad.title == "Updated Title"

    def test_ad_update_non_owner(self, api_client, another_user, test_ad):
        api_client.force_authenticate(user=another_user)
        url = reverse("api:ad_update", kwargs={"pk": test_ad.pk})
        response = api_client.patch(url, {})
        assert response.status_code == status.HTTP_403_FORBIDDEN
