from django.db import models
from apps.main.models import IsActiveMixin


class Teacher(IsActiveMixin):
    name = models.CharField(verbose_name="ФИО", max_length=300)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self) -> str:
        return self.name
