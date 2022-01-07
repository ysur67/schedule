from typing import Dict, Iterable, List, Union
from apps.feedback.bots.utils.const import VK_MAX_BUTTONS_IN_KEYBOARD
from apps.timetables.models.group import Group
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async
from apps.timetables.usecases.educational_level import get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level
from apps.feedback.bots.utils.keyboard import GroupsKeyboard
from django.core.paginator import Paginator


class GetGroupsByLevelCommand(BaseCommand):

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        amount_of_groups = await sync_to_async(groups.count)()
        if amount_of_groups > VK_MAX_BUTTONS_IN_KEYBOARD:
            return await self.build_response_with_multiple_messages(groups)
        return await self.build_response_with_keyboard(groups)

    async def build_response_with_keyboard(self, groups: Iterable[Group]) -> Union[SingleMessage, MultipleMessages]:
        _keyboard = GroupsKeyboard(groups)
        keyboard = await sync_to_async(_keyboard.to_vk_api)()
        return SingleMessage(message="Выберите одну из групп", keyboard=keyboard)

    async def build_response_with_multiple_messages(self, page: Iterable[Group]) -> Union[SingleMessage, MultipleMessages]:
        ITEMS_PER_PAGE = 8
        paginator = Paginator(page.order_by("id"), ITEMS_PER_PAGE)
        result: List[SingleMessage] = []
        pages_range = await sync_to_async(getattr)(paginator, "page_range", [])
        for index in pages_range:
            page = await sync_to_async(paginator.page)(index)
            _keyboard = GroupsKeyboard(page.object_list, is_inline=True)
            keyboard = await sync_to_async(_keyboard.to_vk_api)()
            result.append(SingleMessage(
                message="Выберите одну из групп",
                keyboard=keyboard
            ))
        return MultipleMessages(messages=result)
