from django.db import models
from apps.main.models import BaseModel
from apps.timetables.models import Group, Teacher, Classroom


class Lesson(BaseModel):
    """Модель для описания занятия/пары."""
    date = models.DateField(verbose_name="Дата занятия")
    time_start = models.TimeField(verbose_name="Время начала", null=True)
    time_end = models.TimeField(
        verbose_name="Время окончания занятия", null=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="lessons",
        verbose_name="Группа"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="lessons",
        verbose_name="Преподаватель"
    )
    note = models.TextField(verbose_name="Примечание")
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, related_name="lessons",
        null=True, blank=True,
        verbose_name="Аудитория"
    )
