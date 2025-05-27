from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Настройка Swagger/OpenAPI документации
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",  # Заголовок документации
        default_version="v1",  # Версия API
        description="Документация API для системы обмена товарами",  # Описание
        terms_of_service="https://www.example.com/policies/terms/",  # Условия использования
        contact=openapi.Contact(
            email="a.s.pavlushenko@gmail.com"
        ),  # Контактная информация
        license=openapi.License(name="BSD License"),  # Лицензия
    ),
    public=True,  # Документация доступна без аутентификации
    permission_classes=(permissions.AllowAny,),  # Права доступа к документации
)

# Основные URL-маршруты проекта
urlpatterns = [
    # Админ-панель Django
    path("admin/", admin.site.urls),
    # Подключение URL-маршрутов приложений
    path("", include("main.urls", namespace="main")),  # Основное приложение
    path("", include("users.urls", namespace="users")),  # Приложение пользователей
    path("", include("ads.urls", namespace="ads")),  # Приложение объявлений
    path("api/", include("api.urls", namespace="api")),  # API приложения
    # Документация API
    path(
        "swagger/",  # URL для Swagger UI
        schema_view.with_ui("swagger", cache_timeout=0),  # Интерфейс Swagger
        name="schema-swagger-ui",  # Имя URL
    ),
    path(
        "redoc/",  # URL для ReDoc
        schema_view.with_ui("redoc", cache_timeout=0),  # Интерфейс ReDoc
        name="schema-redoc",  # Имя URL
    ),
]

# В режиме DEBUG добавляем маршруты для медиа-файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
