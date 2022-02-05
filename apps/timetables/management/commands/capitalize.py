from typing import Any, Optional

from django.core.management import BaseCommand

from apps.timetables.models import EducationalLevel


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        levels = EducationalLevel.objects.all()
        for level in levels:
            level.title = level.title.capitalize()
        EducationalLevel.objects.bulk_update(levels, ["title"])
