from django.core.management import BaseCommand
from typing import Any, Optional

from apps.feedback.tasks.lessons import send_notifications_in_lesson_day


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        send_notifications_in_lesson_day()
