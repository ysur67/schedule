from typing import Optional
from apps.timetables.models import Classroom


def get_classroom_by_name(name: str) -> Optional[Classroom]:
    return Classroom.objects.filter(title__iexact=name).first()


def create_classroom(**options) -> Classroom:
    return Classroom.objects.create(**options)
