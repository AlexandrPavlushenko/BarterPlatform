import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAdFilters:
    def test_search_filter(self, client, test_ad):
        response = client.get(reverse("ads:ad_list") + "?search=Test")
        assert test_ad.title.encode() in response.content

    def test_category_filter(self, client, test_ad):
        response = client.get(reverse("ads:ad_list") + "?category=electronics")
        assert test_ad.title.encode() in response.content
