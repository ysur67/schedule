from typing import Dict, Iterable, List, Union
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from apps.feedback.bots.utils.const import VK_MAX_BUTTONS_IN_KEYBOARD
from apps.feedback.bots.utils.keyboard.levels import EducationalLevelsKeyboard
from apps.timetables.models.group import EducationalLevel
from apps.timetables.usecases.educational_level import get_all_educational_levels
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class EducationalLevelsCommand(BaseCommand):

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        levels = get_all_educational_levels()
        amount_of_levels: int = await sync_to_async(levels.count)()
        if amount_of_levels > VK_MAX_BUTTONS_IN_KEYBOARD:
            return await self.build_response_with_multiple_messages()
        _keyboard = EducationalLevelsKeyboard(get_all_educational_levels())
        keyboard = await sync_to_async(_keyboard.to_vk_api)()
        return SingleMessage(message="Выберите один из пунктов меню", keyboard=keyboard)

    async def build_response_with_multiple_messages(self, levels: QuerySet[EducationalLevel]):
        ITEMS_PER_PAGE = 8
        paginator = Paginator(levels.order_by("id"), ITEMS_PER_PAGE)
        result: List[SingleMessage] = []
        pages_range = await sync_to_async(getattr)(paginator, "page_range", [])
        for index in pages_range:
            page = await sync_to_async(paginator.page)(index)
            _keyboard = EducationalLevelsKeyboard(page.object_list, is_inline=True)
            keyboard = await sync_to_async(_keyboard.to_vk_api)()
            result.append(SingleMessage(
                message="Выберите один из пунктов меню",
                keyboard=keyboard
            ))
        return MultipleMessages(messages=result)
