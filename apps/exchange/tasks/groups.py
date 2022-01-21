from project.celery import app as celery_app
from apps.exchange.parse.http import RequestType
from apps.exchange.parse.http.groups import AllGroupsParser
from celery.beat import crontab


@celery_app.task()
def parse_groups_info() -> None:
    parser = AllGroupsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
        payload_data={},
        request_type=RequestType.GET
    )
    return parser.parse()

celery_app.conf.beat_schedule = {
    'parse-groups-info-every-hour': {
        'task': 'apps.exchange.tasks.groups.parse_groups_info',
        'schedule': crontab(hour="*/3"),
    },
}

celery_app.conf.timezone = 'UTC'
