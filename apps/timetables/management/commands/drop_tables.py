from typing import Any, Optional

from django.core.management import BaseCommand

from apps.timetables.models import Classroom, Group, Lesson, Subject, Teacher


class Command(BaseCommand):
    models = (
        Group, Classroom, Lesson, Subject, Teacher
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for model in self.models:
            model.objects.all().delete()
