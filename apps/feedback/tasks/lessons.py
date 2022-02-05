import asyncio
from datetime import date, datetime
from typing import Union

from apps.feedback.bots.base import BaseBot
from apps.feedback.bots.commands.base import MultipleMessages, SingleMessage
from apps.feedback.bots.commands.utils import (build_lessons_message,
                                               get_note_message)
from apps.feedback.bots.vk.bot import VkBot
from apps.feedback.models import Profile
from apps.main.usecases import get_settings
from apps.timetables.usecases.group import get_groups_that_have_lessons_in_date
from apps.timetables.usecases.lesson import get_lessons_by_profile_and_date
from project.celery import app as celery_app


@celery_app.task()
def send_notifications_in_lesson_day() -> None:
    date_ = date.today()
    groups = get_groups_that_have_lessons_in_date(
        date_
    ).prefetch_related("profiles", "lessons")
    if not groups:
        return
    settings = get_settings()
    bot = VkBot(settings.vk_token)
    for profile in Profile.objects.filter(current_group__in=groups).prefetch_related("messenger_accounts"):
        lessons = get_lessons_by_profile_and_date(profile, date_)
        note_message = get_note_message()
        lessons_message = build_lessons_message(
            lessons_by_date={date_: lessons},
            group=profile.get_group(),
            date_start=date_
        )
        account = profile.get_accounts_in_messengers().first()
        asyncio.get_event_loop().run_until_complete(
            bot.send_message(
                MultipleMessages([SingleMessage(note_message), SingleMessage(lessons_message)]),
                int(account.account_id)
            )
        )
