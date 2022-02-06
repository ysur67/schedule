from django.db import models

from .mixins import BaseModel


class ApplicationSettings(BaseModel):
    vk_token = models.CharField(
        verbose_name="Токен для бота ВК",
        max_length=300
    )
    telegram_token = models.CharField(
        verbose_name="Токен для бота Телеграм",
        max_length=300,
        default=""
    )

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = verbose_name
