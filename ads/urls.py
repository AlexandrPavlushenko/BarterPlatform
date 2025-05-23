from django.urls import path

from .apps import AdsConfig
from .views import (
    BarterMainView,
)

app_name = AdsConfig.name

urlpatterns = [
    path("barter_main/", BarterMainView.as_view(), name="barter_main"),
    ]