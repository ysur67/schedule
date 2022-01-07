from typing import Dict
from .base import BaseCommand
from asgiref.sync import sync_to_async
from apps.timetables.usecases.educational_level import get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level
from apps.feedback.bots.utils.keyboard import GroupsKeyboard


class GetGroupsByLevelCommand(BaseCommand):

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _vk_execute(self) -> Dict:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        _keyboard = GroupsKeyboard(groups)
        keyboard = await sync_to_async(_keyboard.to_vk_api)()
        return {
            "message": "Выберите одну из групп",
            "keyboard": keyboard
        }
