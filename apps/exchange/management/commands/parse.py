from typing import Any, Optional

from apps.exchange.parse import LessonsParser
from apps.timetables.models import EducationalLevel
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        levels = get_all_educational_levels()
        for elem in levels:
            self.run_parser(elem)

    def run_parser(self, level: EducationalLevel) -> None:
        payload = {
            "rtype": "3",
            "ucstep": str(level.code),
            "exam": "0",
            "datafrom": "01.01.2022",
            "dataend": "01.08.2022",
            "formo": "2",
            "formob": "0",
            "prdis": "0"
        }
        parser = LessonsParser.build_parser(
            "http://inet.ibi.spb.ru/raspisan/rasp.php",
            payload_data=payload
        )
        parser.parse()
