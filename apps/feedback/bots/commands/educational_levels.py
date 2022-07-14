from typing import Iterable

from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels

from .base import BaseCommand


class EducationalLevelsCommand(BaseCommand):

    async def _execute(self) -> Iterable[SingleMessage]:
        keyboard = EducationalLevelsKeyboard(get_all_educational_levels())
        return [SingleMessage(message="Выберите один из пунктов меню", keyboard=keyboard)]
