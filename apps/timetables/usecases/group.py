from typing import List, Optional
from apps.timetables.models import Group
from apps.timetables.models.group import EducationalLevel


def get_group_by_title(title: str) -> Optional[Group]:
    return Group.objects.filter(title__iexact=title).first()


def create_group(**options) -> Group:
    return Group.objects.create(**options)


def get_all_groups() -> List[Group]:
    return Group.objects.filter(is_active=True)


def get_groups_by_educational_level(level: EducationalLevel) -> List[Group]:
    return Group.objects.filter(level=level)
