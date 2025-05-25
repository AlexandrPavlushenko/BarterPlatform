from django.urls import path

from .apps import AdsConfig
from .views import (AdListView,AdCreateView, AdDetailView, AdUpdateView, AdDeleteView)

app_name = AdsConfig.name

urlpatterns = [
    path('ad_list/', AdListView.as_view(), name='ad_list'),
    path('ad_create/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    # path('proposals/', ProposalListView.as_view(), name='proposal_list'),
    # path('proposals/<int:pk>/', ProposalDetailView.as_view(), name='proposal_detail'),
    # path('<int:ad_pk>/propose/', ProposalCreateView.as_view(), name='proposal_create'),
    # path('proposals/<int:pk>/<str:status>/', ProposalUpdateStatusView.as_view(), name='proposal_update_status'),
]