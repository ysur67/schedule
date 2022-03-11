from typing import Optional

from apps.timetables.models import Teacher
from django.db.models import QuerySet


def get_teacher_by_name(name: str) -> Optional[Teacher]:
    return Teacher.objects.filter(name__icontains=name).first()


def create_teacher(**options) -> Teacher:
    return Teacher.objects.create(**options)


def get_all_teachers() -> QuerySet[Teacher]:
    return Teacher.objects.all()
