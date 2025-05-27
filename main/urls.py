from django.urls import path

from .apps import MainConfig
from .views import IndexView

# Пространство имен для URL-адресов приложения
app_name = MainConfig.name  # 'main'

urlpatterns = [
    # Главная страница приложения
    path("", IndexView.as_view(), name="index")
]
