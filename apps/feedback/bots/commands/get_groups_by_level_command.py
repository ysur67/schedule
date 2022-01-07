from typing import Dict, Iterable
from apps.timetables.models.group import Group
from .base import BaseCommand
from asgiref.sync import sync_to_async
from apps.timetables.usecases.educational_level import get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level
from apps.feedback.bots.utils.keyboard import GroupsKeyboard


class GetGroupsByLevelCommand(BaseCommand):
    VK_MAX_BUTTONS_IN_KEYBOARD = 40

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _vk_execute(self) -> Dict:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        amount_of_groups = await sync_to_async(groups.count)()
        if amount_of_groups > self.VK_MAX_BUTTONS_IN_KEYBOARD:
            return await self.build_response_with_text(groups)
        return await self.build_response_with_keyboard(groups)


    async def build_response_with_keyboard(self, groups: Iterable[Group]) -> Dict:
        _keyboard = GroupsKeyboard(groups)
        keyboard = await sync_to_async(_keyboard.to_vk_api)()
        return {
            "message": "Выберите одну из групп",
            "keyboard": keyboard
        }

    async def build_response_with_text(self, groups: Iterable[Group]) -> Dict:
        message = "Упс, кажется на этом уровне слишком много групп...\n"
        message += "К сожалению, тебе придется выбрать ее из предложенного списка "
        message += "и написать ее самому.\n"
        message = await sync_to_async(self._build_message)(message, groups)
        return {
            "message": message
        }

    def _build_message(self, message: str, groups: Iterable[Group]) -> str:
        OFFSET = 10
        for index, item in enumerate(groups):
            message += f"{item.title}"
            if not index == len(groups) - 1:
                message += ", "
        return message
