from apps.exchange.parse.http.lessons_main_site import LessonsParser
from project.celery import app as celery_app
from celery.beat import crontab


@celery_app.task()
def parse_groups_info() -> None:
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


celery_app.conf.beat_schedule = {
    'parse-lessons-info-every-hour': {
        'task': 'apps.exchange.tasks.groups.parse_groups_info',
        'schedule': crontab(hour="*/1"),
    },
}

celery_app.conf.timezone = 'UTC'
