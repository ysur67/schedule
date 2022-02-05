from django.db import models

from apps.main.models import BaseModel


class EducationalLevel(BaseModel):
    """Модель для описания уровня образования."""

    code = models.CharField(verbose_name="Код", max_length=300, default="")

    class Meta:
        verbose_name = "Уровень образования"
        verbose_name_plural = "Уровни образования"

    def to_logging_message(self) -> str:
        msg = super().to_logging_message()
        msg += f"Код: {self.code}"
        return msg


class Group(BaseModel):
    """Модель для описания группы студентов."""

    level = models.ForeignKey(
        EducationalLevel, verbose_name="Уровень образования",
        on_delete=models.SET_NULL, related_name="groups",
        null=True
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def to_logging_message(self) -> str:
        msg = super().to_logging_message()
        msg += f"Уровень образования: {self.level}"
        return msg
