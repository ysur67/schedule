from typing import Optional

from apps.timetables.models import Subject


def get_subject_by_title(title: str) -> Optional[Subject]:
    return Subject.objects.filter(title__iexact=title).first()


def create_subject(**options) -> Subject:
    return Subject.objects.create(**options)
