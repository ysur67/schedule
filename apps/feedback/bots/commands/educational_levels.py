from typing import Iterable, Union

from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels

from .base import BaseCommand, SingleMessage


class EducationalLevelsCommand(BaseCommand):

    async def _execute_for_messengers(self) -> Iterable[SingleMessage]:
        keyboard = EducationalLevelsKeyboard(get_all_educational_levels())
        return SingleMessage(message="Выберите один из пунктов меню", keyboard=keyboard)
