from django.contrib import admin
from apps.feedback.models import Profile, MessengerAccount,  MessengerModel


@admin.register(MessengerModel)
class MessengerModelAdmin(admin.ModelAdmin):
    pass


class MessengerAccountInline(admin.TabularInline):
    model = MessengerAccount
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (MessengerAccountInline,)


@admin.register(MessengerAccount)
class MessengerAccountAdmin(admin.ModelAdmin):
    pass
