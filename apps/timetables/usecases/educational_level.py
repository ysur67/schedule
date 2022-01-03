from typing import List, Optional
from apps.timetables.models import EducationalLevel


def get_educational_level_by_title(title: str) -> Optional[EducationalLevel]:
    return EducationalLevel.objects.filter(title__iexact=title).first()


def create_educational_level(**options) -> EducationalLevel:
    return EducationalLevel.objects.create(**options)

def get_all_educational_levels() -> List[EducationalLevel]:
    return EducationalLevel.objects.filter(is_active=True)
