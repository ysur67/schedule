from datetime import date, timedelta
from typing import Iterable

from apps.feedback.bots.commands.utils import build_lessons_message
from apps.main.utils.date import to_message_format
from apps.timetables.usecases.lesson import \
    get_lessons_dict_by_group_and_date_range
from asgiref.sync import sync_to_async

from .base import CommandWithProfile, SingleMessage


class GetScheduleCommand(CommandWithProfile):

    @property
    def date_start(self) -> date:
        return self._require_field("date_start")

    @property
    def date_end(self) -> date:
        return self._require_field("date_end", raise_exception=False)

    async def _execute_for_messengers(self) -> Iterable[SingleMessage]:
        group = await sync_to_async(self.profile.get_group)()
        if not group:
            result = "У тебя не выбрана группа.\n"
            result += "Я не могу показать тебе расписание, если я не знаю твоей группы"
            return [SingleMessage(message=result)]
        date_start = self.date_start
        date_end = self.date_end or date_start + \
            timedelta(days=self.profile.days_offset)
        lessons = await sync_to_async(get_lessons_dict_by_group_and_date_range)(group, date_start, date_end)
        if not lessons:
            result = f"Кажется у тебя нет пар c {to_message_format(date_start)} "
            result += f"по {to_message_format(date_end)}, "
            result += "но все же проверь информацию..."
            return [SingleMessage(message=result)]
        _build_message = sync_to_async(build_lessons_message)
        result = await _build_message(lessons, group, date_start, date_end)
        return [SingleMessage(message=item) for item in result]
