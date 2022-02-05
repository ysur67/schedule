from typing import Union

from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels

from .base import BaseCommand, MultipleMessages, SingleMessage


class EducationalLevelsCommand(BaseCommand):

    async def _execute_for_messengers(self) -> Union[SingleMessage, MultipleMessages]:
        keyboard = EducationalLevelsKeyboard(get_all_educational_levels())
        return SingleMessage(message="Выберите один из пунктов меню", keyboard=keyboard)
