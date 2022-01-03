from django.db import models
from .mixins import BaseModel


class ApplicationSettings(BaseModel):
    vk_token = models.CharField(
        verbose_name="Токен для бота ВК",
        max_length=300
    )

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = verbose_name
