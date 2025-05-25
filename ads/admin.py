from django.contrib import admin
from django.utils.html import format_html
from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'condition', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('category', 'condition', 'created_at', 'author')
    search_fields = ('title', 'description')
    list_per_page = 6

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender', 'receiver_user', 'ad', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('ad__title', 'comment')
    list_per_page = 20

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'accepted': 'green',
            'rejected': 'red'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 10px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )

    status_badge.short_description = "Статус"

    # def mark_as_accepted(self, request, queryset):
    #     queryset.update(status='accepted')
    # mark_as_accepted.short_description = "Пометить как принятые"
    #
    # def mark_as_rejected(self, request, queryset):
    #     queryset.update(status='rejected')
    # mark_as_rejected.short_description = "Пометить как отклоненные"
