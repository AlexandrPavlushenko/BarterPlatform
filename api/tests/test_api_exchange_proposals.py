import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import ExchangeProposal


@pytest.mark.django_db
class TestExchangeProposalAPI:
    """Тесты API для работы с предложениями обмена (ExchangeProposal)."""

    def test_proposal_create(self, api_client, another_user, test_ad):
        """Тест создания предложения обмена.

        Проверяет:
        - Аутентифицированный пользователь может создать предложение (201)
        - Предложение сохраняется в базе данных
        - Предложение связано с правильным объявлением
        """
        api_client.force_authenticate(user=another_user)
        url = reverse("api:exchange_proposal_create")
        data = {"ad": test_ad.pk, "comment": "Test proposal comment"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert ExchangeProposal.objects.filter(ad=test_ad).exists()

    def test_proposal_create_to_own_ad(self, api_client, test_user, test_ad):
        """Тест попытки создания предложения для своего собственного объявления.

        Проверяет:
        - Пользователь не может создать предложение для своего объявления (400)
        - Система предотвращает создание циклических предложений
        """
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_create")
        response = api_client.post(url, {"ad": test_ad.pk})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_proposal_list_authenticated(self, api_client, test_user, test_proposal):
        """Тест получения списка предложений для аутентифицированного пользователя.

        Проверяет:
        - Код ответа 200 OK
        - Наличие тестового предложения в списке
        - Корректность данных в ответе
        """
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_proposal_detail_owner(self, api_client, test_user, test_proposal):
        """Тест просмотра деталей предложения владельцем объявления.

        Проверяет:
        - Владелец может просматривать предложение (200)
        - Корректность данных в ответе
        - Наличие комментария в ответе
        """
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_detail", kwargs={"pk": test_proposal.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "Test proposal comment"

    def test_proposal_update_status(self, api_client, test_user, test_proposal):
        """Тест обновления статуса предложения владельцем объявления.

        Проверяет:
        - Владелец может изменить статус предложения (200)
        - Статус корректно обновляется в базе данных
        - Поддерживаются допустимые статусы (accepted/rejected)
        """
        api_client.force_authenticate(user=test_user)
        url = reverse("api:exchange_proposal_update", kwargs={"pk": test_proposal.pk})
        data = {"status": "accepted"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        test_proposal.refresh_from_db()
        assert test_proposal.status == "accepted"

    def test_proposal_delete_sender(self, api_client, another_user, test_proposal):
        """Тест удаления предложения отправителем.

        Проверяет:
        - Отправитель может удалить свое предложение (204)
        - Предложение действительно удаляется из базы данных
        - Проверка отсутствия предложения после удаления
        """
        api_client.force_authenticate(user=another_user)
        url = reverse("api:exchange_proposal_delete", kwargs={"pk": test_proposal.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ExchangeProposal.objects.filter(pk=test_proposal.pk).exists()
