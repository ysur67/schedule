from typing import Any, Dict, Iterable, List, Union
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async
from apps.timetables.usecases.educational_level import get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level
from apps.feedback.bots.utils.keyboard import GroupsKeyboard
from functools import singledispatchmethod


class GetGroupsByLevelCommand(BaseCommand):

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        _keyboard = GroupsKeyboard(groups)
        keyboard_data = await sync_to_async(_keyboard.to_vk_api)()
        return await self.build_response(keyboard_data)

    @singledispatchmethod
    async def build_response(self, keyboard_data: Any) -> Union[SingleMessage, MultipleMessages]:
        raise NotImplementedError(f"There is no approach for type {type(keyboard_data)}")

    @build_response.register(str)
    async def _(self, keyboard_data: str) -> SingleMessage:
        return SingleMessage(message="Выберите одну из групп", keyboard=keyboard_data)

    @build_response.register(list)
    async def _(self, keyboard_data: List[str]) -> MultipleMessages:
        result: List[SingleMessage] = []
        for keyboard in keyboard_data:
            keyboard_response = await self.build_response(keyboard)
            result.append(keyboard_response)
        return MultipleMessages(messages=result)
