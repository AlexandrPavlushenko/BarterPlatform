from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic


class IndexView(generic.TemplateView):
    """Представление главной страницы приложения.

    Обрабатывает два сценария:
    1. Для неавторизованных пользователей - отображает стартовую страницу
    2. Для авторизованных пользователей - перенаправляет на список объявлений

    Атрибуты:
        template_name (str): Путь к шаблону стартовой страницы (main/index.html)

    Методы:
        dispatch: Переопределяет стандартное поведение для реализации перенаправления
    """

    # Шаблон для отображения главной страницы
    template_name = "main/index.html"

    def dispatch(self, request, *args, **kwargs):
        """Обрабатывает входящий запрос с проверкой аутентификации.

        Args:
            request: Объект HTTP-запроса
            *args: Дополнительные позиционные аргументы
            **kwargs: Дополнительные именованные аргументы

        Returns:
            HttpResponse:
                - Перенаправление на ads:ad_list для авторизованных пользователей
                - Обычный рендеринг шаблона для гостей
        """
        # Проверяем статус аутентификации пользователя
        if request.user.is_authenticated:
            # Перенаправляем авторизованных пользователей
            return redirect(reverse("ads:ad_list"))
        # Для неавторизованных - стандартная обработка
        return super().dispatch(request, *args, **kwargs)
