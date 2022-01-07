from typing import Dict

from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.timetables.usecases.educational_level import get_all_educational_levels
from .base import BaseCommand
from asgiref.sync import sync_to_async


class EducationalLevelsCommand(BaseCommand):

    async def _vk_execute(self) -> Dict:
        _keyboard = EducationalLevelsKeyboard(get_all_educational_levels())
        keyboard = await sync_to_async(_keyboard.to_vk_api)()
        return {
            "message": "Выберите один из пунктов меню",
            "keyboard": keyboard
        }
