import pytest
from django.urls import reverse

from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
class TestAdViews:
    """Тестирование представлений (views) для работы с объявлениями."""

    def test_ad_list_view(self, client, test_ad):
        """Проверяет отображение списка объявлений.

        Args:
            client: Тестовый клиент Django
            test_ad: Фикстура тестового объявления

        Asserts:
            - Статус код ответа 200 (OK)
            - Заголовок тестового объявления присутствует на странице
        """
        response = client.get(reverse("ads:ad_list"))
        assert response.status_code == 200
        assert test_ad.title.encode() in response.content

    def test_ad_detail_view(self, client, test_ad):
        """Проверяет отображение детальной страницы объявления.

        Args:
            client: Тестовый клиент Django
            test_ad: Фикстура тестового объявления

        Asserts:
            - Статус код ответа 200 (OK)
            - Заголовок объявления присутствует на странице
        """
        response = client.get(reverse("ads:ad_detail", kwargs={"pk": test_ad.pk}))
        assert response.status_code == 200
        assert test_ad.title.encode() in response.content

    def test_ad_create_view(self, client, test_user):
        """Проверяет создание нового объявления.

        Args:
            client: Тестовый клиент Django
            test_user: Фикстура авторизованного пользователя

        Asserts:
            - После успешного создания происходит редирект (код 302)
            - Новое объявление появляется в базе данных
        """
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
    """Тестирование представлений для работы с предложениями обмена."""

    def test_proposal_create_view(self, client, test_user, test_ad):
        """Проверяет создание предложения обмена.

        Args:
            client: Тестовый клиент Django
            test_user: Фикстура авторизованного пользователя (отправитель)
            test_ad: Фикстура тестового объявления

        Asserts:
            - После создания происходит редирект (код 302)
            - Предложение появляется в базе данных с правильными связями
        """
        client.force_login(test_user)
        response = client.post(
            reverse("ads:exchange_create", kwargs={"ad_id": test_ad.pk}),
            {"comment": "Test proposal"},
        )
        assert response.status_code == 302
        assert ExchangeProposal.objects.filter(ad=test_ad, ad_sender=test_user).exists()

    def test_accept_proposal_view(self, client, test_user, test_proposal):
        """Проверяет принятие предложения обмена.

        Args:
            client: Тестовый клиент Django
            test_user: Фикстура авторизованного пользователя (получатель)
            test_proposal: Фикстура тестового предложения

        Asserts:
            - Статус предложения меняется на 'accepted'
            - После обработки происходит редирект (код 302)
        """
        client.force_login(test_user)
        response = client.post(
            reverse("ads:accept_proposal", kwargs={"pk": test_proposal.pk})
        )
        test_proposal.refresh_from_db()
        assert test_proposal.status == "accepted"
        assert response.status_code == 302
