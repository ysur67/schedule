from typing import Iterable

from apps.feedback.bots.utils.keyboard.base import Button, SimpleKeyboard
from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from apps.timetables.models.group import EducationalLevel
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels
from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from .base import BaseCommand


class EducationalLevelsCommand(BaseCommand):

    async def _execute(self) -> Iterable[SingleMessage]:
        levels = await sync_to_async(list)(get_all_educational_levels())
        keyboard = SimpleKeyboard(
            data=educational_levels_to_buttons(levels)
        )
        return [SingleMessage(message="Выберите один из пунктов меню", keyboard=keyboard)]


def educational_levels_to_buttons(
    levels: QuerySet[EducationalLevel]
) -> 'list[EducationalLevel]':
    return [Button(title=item.title) for item in levels]
