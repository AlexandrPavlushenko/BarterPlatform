from django.urls import path

from .apps import AdsConfig
from .views import (AcceptProposalView, AdCreateView, AdDeleteView,
                    AdDetailView, AdListView, AdUpdateView,
                    ExchangeProposalCreateView, ExchangeProposalDeleteView,
                    RejectProposalView)

"""
URL-маршруты для приложения объявлений (ads).

Этот модуль определяет все URL-шаблоны для работы с:
- Объявлениями (создание, просмотр, редактирование, удаление)
- Предложениями обмена (создание, удаление, принятие/отклонение)

Основные группы маршрутов:
1. Маршруты объявлений:
   - /ad_list/ - список всех объявлений
   - /ad_create/ - создание нового объявления
   - /<pk>/ - детализация объявления
   - /<pk>/update/ - редактирование объявления
   - /<pk>/delete/ - удаление объявления

2. Маршруты предложений обмена:
   - /ad/<ad_id>/exchange/ - создание предложения обмена
   - /proposal/delete/<pk>/ - удаление предложения
   - /proposal/<pk>/accept/ - принятие предложения
   - /proposal/<pk>/reject/ - отклонение предложения

Пространство имен приложения: 'ads' (используется для reverse-поиска URL)
"""

app_name = AdsConfig.name

urlpatterns = [
    path("ad_list/", AdListView.as_view(), name="ad_list"),
    path("ad_create/", AdCreateView.as_view(), name="ad_create"),
    path("<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("<int:pk>/update/", AdUpdateView.as_view(), name="ad_update"),
    path("<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
    path(
        "ad/<int:ad_id>/exchange/",
        ExchangeProposalCreateView.as_view(),
        name="exchange_create",
    ),
    path(
        "proposal/delete/<int:pk>/",
        ExchangeProposalDeleteView.as_view(),
        name="proposal_delete",
    ),
    path(
        "proposal/<int:pk>/accept/",
        AcceptProposalView.as_view(),
        name="accept_proposal",
    ),
    path(
        "proposal/<int:pk>/reject/",
        RejectProposalView.as_view(),
        name="reject_proposal",
    ),
]
