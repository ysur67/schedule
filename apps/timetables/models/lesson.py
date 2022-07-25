from apps.main.models import BaseModel
from apps.timetables.models import Classroom, Group, Subject, Teacher
from django.db import models


class Lesson(BaseModel):
    """Модель для описания занятия/пары."""
    date = models.DateField(verbose_name="Дата занятия")
    time_start = models.TimeField(
        verbose_name="Время начала",
        null=True, blank=True
    )
    time_end = models.TimeField(
        verbose_name="Время окончания занятия",
        null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="lessons",
        verbose_name="Группа"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="lessons",
        verbose_name="Преподаватель"
    )
    note = models.TextField(verbose_name="Примечание", null=True)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, related_name="lessons",
        null=True, blank=True,
        verbose_name="Аудитория"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, related_name="lessons",
        null=True, verbose_name="Дисциплина"
    )
    href = models.CharField(
        max_length=1000,
        null=True, blank=True,
        verbose_name='Ссылка'
    )

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def to_logging_message(self) -> str:
        msg = super().to_logging_message()
        msg += f"Дата: {self.date}\n" + \
            f"Время: {self.time_start} - {self.time_end}\n" + \
            f"Группа: {self.group}\n" + \
            f"Преподаватель: {self.teacher}\n" + \
            f"Аудитория: {self.classroom}\n" + \
            f"Дисциплина: {self.subject}"
        return msg
