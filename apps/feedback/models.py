from django.db import models
from apps.main.models.mixins import BaseModel


class Profile(BaseModel):

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.title


class MessengerModel(BaseModel):
    code = models.CharField(
        verbose_name="Код", max_length=300, default="", unique=True
    )

    class Meta:
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры"

    def __str__(self) -> str:
        return self.title


class MessengerAccount(BaseModel):
    messenger = models.ForeignKey(
        MessengerModel, on_delete=models.CASCADE,
        related_name="account", verbose_name="Мессенджер"
    )
    account_id = models.CharField(
        verbose_name="Идентификатор аккаунта в мессенджере",
        max_length=300
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name="messenger_accounts", verbose_name="Профиль"
    )

    class Meta:
        verbose_name = "Аккаунт в мессенджере"
        verbose_name_plural = "Аккаунты в мессенджере"

    def __str__(self) -> str:
        return self.profile.title
