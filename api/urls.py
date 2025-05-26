from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .apps import ApiConfig
from .views import (
    AdCreateView,
    AdDeleteView,
    AdDetailView,
    AdListView,
    AdUpdateView,
    MyTokenObtainPairView,
    ExchangeProposalDeleteView,
    ExchangeProposalListView,
    ExchangeProposalCreateView,
    ExchangeProposalDetailView,
    ExchangeProposalUpdateView,
    UserRegisterView,
)

app_name = ApiConfig.name

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("ad_list/", AdListView.as_view(), name="ad_list"),
    path("ad_detail/<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("ad_create/", AdCreateView.as_view(), name="ad_create"),
    path("ad_update/<int:pk>/", AdUpdateView.as_view(), name="ad_update"),
    path("ad_delete/<int:pk>/", AdDeleteView.as_view(), name="ad_delete"),
    path(
        "exchange_proposal_delete/<int:pk>/",
        ExchangeProposalDeleteView.as_view(),
        name="exchange_proposal_delete",
    ),
    path(
        "exchange_proposal_list/",
        ExchangeProposalListView.as_view(),
        name="exchange_proposal_list",
    ),
    path(
        "exchange_proposal_detail/<int:pk>/",
        ExchangeProposalDetailView.as_view(),
        name="exchange_proposal_detail",
    ),
    path(
        "exchange_proposal_create/",
        ExchangeProposalCreateView.as_view(),
        name="exchange_proposal_create",
    ),
    path(
        "exchange_proposal_update/<int:pk>/",
        ExchangeProposalUpdateView.as_view(),
        name="exchange_proposal_update",
    ),
]
