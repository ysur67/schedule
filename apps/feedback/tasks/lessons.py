from apps.feedback.bots.commands.utils import build_lessons_message
from apps.feedback.models import Profile
from apps.timetables.usecases.group import get_groups_that_have_lessons_in_date
from apps.timetables.usecases.lesson import get_lessons_by_profile_and_date
from project.celery import app as celery_app
from celery.beat import crontab
from datetime import date, datetime


@celery_app.task()
def send_notifications_in_lesson_day() -> None:
    # date_ = date.today()
    date_ = datetime.strptime("01.02.2022", "%d.%m.%Y").date()
    groups = get_groups_that_have_lessons_in_date(
        date_
    ).prefetch_related("profiles", "lessons")
    for profile in Profile.objects.filter(current_group__in=groups):
        lessons = get_lessons_by_profile_and_date(profile, date_)
        note_message = "Привет!\n"
        note_message += "Ты попросил отправлять тебе уведомления о занятиях "
        note_message += "в день их проведения.\n"
        note_message += "Поэтому ниже отправляю тебе твои занятия на сегодня.\n"
        note_message += "Ты всегда можешь отключить уведомления в настройках"
        lessons_message = build_lessons_message({
            date_: lessons,
        }, profile.current_group, date_, date_)

