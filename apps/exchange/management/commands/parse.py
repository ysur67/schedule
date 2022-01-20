from typing import Any, Optional
from django.core.management.base import BaseCommand
from apps.exchange.parse import LessonsParser


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        payload = {
            "rtype": "3",
            "ucstep": "1",
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
