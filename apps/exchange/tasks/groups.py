from apps.exchange.usecases.exchange_settings import get_exchange_settings
from project.celery import app as celery_app
from apps.exchange.parse.http import RequestType
from apps.exchange.parse.http.groups import AllGroupsParser
from celery.beat import crontab


@celery_app.task()
def parse_groups_info() -> None:
    settings = get_exchange_settings()
    if not settings:
        raise ValueError("There is no exchange settings provided")
    if not settings.is_parsing_enabled:
        return print("info parsing is turned off")
    parser = AllGroupsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
        payload_data={},
        request_type=RequestType.GET
    )
    return parser.parse()
