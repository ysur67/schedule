from datetime import date
from typing import List, Optional

from django.db.models import QuerySet

from apps.timetables.models import Group
from apps.timetables.models.group import EducationalLevel


def get_group_by_title(title: str) -> Optional[Group]:
    return Group.objects.filter(title__iexact=title).first()


def create_group(**options) -> Group:
    return Group.objects.create(**options)


def get_all_groups() -> List[Group]:
    return Group.objects.filter(is_active=True)


def get_groups_by_educational_level(level: EducationalLevel) -> List[Group]:
    return get_all_groups().filter(level=level)


def get_groups_that_have_lessons_in_date(date: date) -> QuerySet[Group]:
    return Group.objects.filter(
        lessons__date=date
    ).distinct("title")
