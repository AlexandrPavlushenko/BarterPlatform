from django.urls import path

from .apps import AdsConfig
from .views import (AcceptProposalView, AdCreateView, AdDeleteView,
                    AdDetailView, AdListView, AdUpdateView,
                    ExchangeProposalCreateView, ExchangeProposalDeleteView,
                    RejectProposalView)

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
