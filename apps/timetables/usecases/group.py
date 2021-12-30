from typing import Optional
from apps.timetables.models import Group


def get_group_by_title(title: str) -> Optional[Group]:
    return Group.objects.filter(title__iexact=title).first()


def create_group(**options) -> Group:
    return Group.objects.create(**options)
