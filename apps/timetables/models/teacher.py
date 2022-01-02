from django.db import models
from apps.main.models import IsActiveMixin, LoggingMixin


class Teacher(IsActiveMixin, LoggingMixin):
    name = models.CharField(verbose_name="ФИО", max_length=300)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self) -> str:
        return self.name

    def to_logging_message(self) -> str:
        msg = f"Объект: {self._meta.verbose_name}\n" + \
            f"Имя: {self.name}"
        return msg
