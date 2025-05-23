from django.views import generic


class BarterMainView(generic.TemplateView):
    """Представление для главной страницы"""

    template_name = "ads/barter_main.html"

