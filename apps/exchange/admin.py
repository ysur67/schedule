from django.contrib import admin

from apps.exchange.models import ExchangeSettings


@admin.register(ExchangeSettings)
class ExchangeSettingsAdmin(admin.ModelAdmin):
    pass
