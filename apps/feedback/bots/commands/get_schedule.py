from typing import Union

from apps.feedback.bots.commands.utils import build_lesson_message
from apps.timetables.usecases.lesson import get_lessons_by_group_and_date_range
from .base import CommandWithProfile, MultipleMessages, SingleMessage
from datetime import date
from asgiref.sync import sync_to_async


class GetScheduleCommand(CommandWithProfile):

    @property
    def date_start(self) -> date:
        return self._require_field("date_start")

    @property
    def date_end(self) -> date:
        return self._require_field("date_end", raise_exception=False)

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        group = await sync_to_async(self.profile.get_group)()
        if not group:
            result = "Упс, у тебя не выбрана группа.\n"
            result += "Я не могу показать тебе расписание, если я не знаю твоей группы"
            return SingleMessage(message=result)
        lessons = await sync_to_async(list)(get_lessons_by_group_and_date_range(group, self.date_start))
        _build_message = sync_to_async(build_lesson_message)
        result = "========\n".join([await _build_message(item) for item in lessons])
        if not result:
            result = "Упс, кажется у тебя нет пар на текущую неделю, "
            result += "но все же проверь информацию..."
        return SingleMessage(message=result)
