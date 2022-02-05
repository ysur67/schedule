from typing import Optional

from apps.timetables.models import Teacher


def get_teacher_by_name(name: str) -> Optional[Teacher]:
    return Teacher.objects.filter(name__icontains=name).first()


def create_teacher(**options) -> Teacher:
    return Teacher.objects.create(**options)
