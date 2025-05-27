from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .apps import ApiConfig
from .views import (AdCreateView, AdDeleteView, AdDetailView, AdListView,
                    AdUpdateView, ExchangeProposalCreateView,
                    ExchangeProposalDeleteView, ExchangeProposalDetailView,
                    ExchangeProposalListView, ExchangeProposalUpdateView,
                    MyTokenObtainPairView, UserRegisterView)

app_name = ApiConfig.name  # Пространство имен для URL API ('api')

urlpatterns = [
    # Аутентификация и регистрация
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Маршруты для работы с объявлениями (Ad)
    path("ad_list/", AdListView.as_view(), name="ad_list"),  # Список всех объявлений
    path(
        "ad_detail/<int:pk>/", AdDetailView.as_view(), name="ad_detail"
    ),  # Детали объявления
    path("ad_create/", AdCreateView.as_view(), name="ad_create"),  # Создание объявления
    path(
        "ad_update/<int:pk>/", AdUpdateView.as_view(), name="ad_update"
    ),  # Обновление объявления
    path(
        "ad_delete/<int:pk>/", AdDeleteView.as_view(), name="ad_delete"
    ),  # Удаление объявления
    # Маршруты для работы с предложениями обмена (ExchangeProposal)
    path(
        "exchange_proposal_delete/<int:pk>/",
        ExchangeProposalDeleteView.as_view(),
        name="exchange_proposal_delete",
    ),  # Удаление предложения
    path(
        "exchange_proposal_list/",
        ExchangeProposalListView.as_view(),
        name="exchange_proposal_list",
    ),  # Список предложений
    path(
        "exchange_proposal_detail/<int:pk>/",
        ExchangeProposalDetailView.as_view(),
        name="exchange_proposal_detail",
    ),  # Детали предложения
    path(
        "exchange_proposal_create/",
        ExchangeProposalCreateView.as_view(),
        name="exchange_proposal_create",
    ),  # Создание предложения
    path(
        "exchange_proposal_update/<int:pk>/",
        ExchangeProposalUpdateView.as_view(),
        name="exchange_proposal_update",
    ),  # Обновление статуса предложения
]
