from django.contrib import admin
from django.utils.html import format_html

from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления объявлениями (Ad).

    Настройки:
    - Отображение списка с превью изображений
    - Фильтрация по категориям, состоянию и дате
    - Поиск по заголовку и описанию
    - Пагинация по 6 элементов на страницу
    """

    list_display = (
        "id",
        "title",
        "author",
        "category",
        "condition",
        "image_preview",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "condition", "created_at", "author")
    search_fields = ("title", "description")
    list_per_page = 6

    def image_preview(self, obj):
        """Генерирует HTML-превью изображения для отображения в списке.

        Args:
            obj: Экземпляр модели Ad

        Returns:
            str: HTML-код изображения или текст "Нет изображения"
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url,
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления предложениями обмена.

    Настройки:
    - Отображение списка с цветными статусами
    - Фильтрация по статусу и дате создания
    - Поиск по заголовку объявления и комментарию
    - Пагинация по 20 элементов на страницу
    """

    list_display = (
        "id",
        "ad_sender",
        "receiver_user",
        "ad",
        "status_badge",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("ad__title", "comment")
    list_per_page = 20

    def status_badge(self, obj):
        """Генерирует цветной бейдж для отображения статуса.

        Args:
            obj: Экземпляр модели ExchangeProposal

        Returns:
            str: HTML-код цветного бейджа со статусом
        """
        colors = {"pending": "orange", "accepted": "green", "rejected": "red"}
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 10px;">{}</span>',
            colors.get(obj.status, "gray"),
            obj.get_status_display(),
        )

    status_badge.short_description = "Статус"

    # def mark_as_accepted(self, request, queryset):
    #     """Массовое действие для пометки предложений как принятых."""
    #     queryset.update(status='accepted')
    # mark_as_accepted.short_description = "Пометить как принятые"
    #
    # def mark_as_rejected(self, request, queryset):
    #     """Массовое действие для пометки предложений как отклоненных."""
    #     queryset.update(status='rejected')
    # mark_as_rejected.short_description = "Пометить как отклоненные"
