from django.db import models
from django.utils.timezone import now


class ExchangeSettings(models.Model):
    is_parsing_enabled = models.BooleanField(
        verbose_name="Парсинг активирован?",
        default=True
    )
    lessons_start_date = models.DateField(
        verbose_name="Дата начала для парсинга занятий",
        default=now
    )
    lesson_end_date = models.DateField(
        verbose_name="Конечная дата для парсинга занятий",
        default=now
    )

    class Meta:
        verbose_name = "Настройки парсинга"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self._meta.verbose_name
