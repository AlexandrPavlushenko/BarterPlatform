import random

from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic


class IndexView(generic.TemplateView):
    """Представление для главной страницы"""

    template_name = "main/index.html"

    # Если пользователь авторизован, перенаправляем его на страницу обмена
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("ads:ad_list"))
        return super().dispatch(request, *args, **kwargs)