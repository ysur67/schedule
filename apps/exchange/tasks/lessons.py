from celery.beat import crontab

from apps.exchange.parse.http.lessons_main_site import LessonsParser
from apps.exchange.usecases.exchange_settings import get_exchange_settings
from apps.main.utils.date import to_message_format
from project.celery import app as celery_app


@celery_app.task()
def parse_lessons_info() -> None:
    settings = get_exchange_settings()
    if not settings:
        raise ValueError("There is no exchange settings provided")
    if not settings.is_parsing_enabled:
        return print("info parsing is turned off")
    payload = {
        "rtype": "3",
        "ucstep": "1",
        "exam": "0",
        "datafrom": to_message_format(settings.lessons_start_date),
        "dataend": to_message_format(settings.lesson_end_date),
        "formo": "2",
        "formob": "0",
        "prdis": "0"
    }
    parser = LessonsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/rasp.php",
        payload_data=payload
    )
    parser.parse()
