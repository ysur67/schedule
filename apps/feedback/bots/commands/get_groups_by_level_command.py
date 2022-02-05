from functools import singledispatchmethod
from typing import Any, Dict, Iterable, List, Union

from asgiref.sync import sync_to_async

from apps.feedback.bots.utils.keyboard import GroupsKeyboard
from apps.timetables.usecases.educational_level import \
    get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level

from .base import BaseCommand, MultipleMessages, SingleMessage


class GetGroupsByLevelCommand(BaseCommand):

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _execute_for_messengers(self) -> Union[SingleMessage, MultipleMessages]:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        keyboard = GroupsKeyboard(groups)
        return SingleMessage(
            message="Выберите одну из групп",
            keyboard=keyboard
        )
