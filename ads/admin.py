from django.contrib import admin
from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'condition', 'image', 'created_at', 'updated_at')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'author__username')


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('ad_sender', 'ad_receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('ad_sender__username', 'ad_receiver__title', 'comment')

    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_editable = ('status',)
