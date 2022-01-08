from typing import Union
from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.timetables.usecases.educational_level import get_all_educational_levels
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class EducationalLevelsCommand(BaseCommand):

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        _keyboard = EducationalLevelsKeyboard(get_all_educational_levels())
        keyboard = await sync_to_async(_keyboard.to_vk_api)()
        return SingleMessage(message="Выберите один из пунктов меню", keyboard=keyboard)
