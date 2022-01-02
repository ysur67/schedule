from typing import Any, Optional
from django.core.management import BaseCommand
from apps.exchange.parse.http import GroupsParser, RequestType


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        parser = GroupsParser.build_parser(
            "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
            payload_data={},
            request_type=RequestType.GET
            )
        parser.parse()
