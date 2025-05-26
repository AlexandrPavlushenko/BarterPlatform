from django.urls import path

from .apps import MainConfig
from .views import IndexView

app_name = MainConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
