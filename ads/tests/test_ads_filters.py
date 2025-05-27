import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAdFilters:
    """Тестирование фильтров списка объявлений."""

    def test_search_filter(self, client, test_ad):
        """Проверяет работу поискового фильтра по заголовку объявления.

        Args:
            client: Тестовый клиент Django
            test_ad: Фикстура тестового объявления

        Asserts:
            - Что объявление с искомым заголовком присутствует в результатах
        """
        response = client.get(reverse("ads:ad_list") + "?search=Test")
        assert test_ad.title.encode() in response.content

    def test_category_filter(self, client, test_ad):
        """Проверяет фильтрацию объявлений по категории.

        Args:
            client: Тестовый клиент Django
            test_ad: Фикстура тестового объявления

        Asserts:
            - Что объявление из указанной категории присутствует в результатах
        """
        response = client.get(reverse("ads:ad_list") + "?category=electronics")
        assert test_ad.title.encode() in response.content
