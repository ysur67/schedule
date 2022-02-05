from typing import Any, Optional

from django.core.management import BaseCommand

from apps.exchange.parse.http import RequestType
from apps.exchange.parse.http.groups import AllGroupsParser


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        parser = AllGroupsParser.build_parser(
            "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
            payload_data={},
            request_type=RequestType.GET
            )
        parser.parse()
