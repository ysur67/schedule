from django.contrib import admin

from apps.main.models import ApplicationSettings


@admin.register(ApplicationSettings)
class SettingsAdmin(admin.ModelAdmin):
    pass
