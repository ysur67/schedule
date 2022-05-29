from functools import singledispatchmethod
from typing import Any, Dict, Iterable, List, Union

from apps.feedback.bots.utils.keyboard import GroupsKeyboard
from apps.timetables.usecases.educational_level import \
    get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level
from asgiref.sync import sync_to_async

from .base import BaseCommand, SingleMessage


class GetGroupsByLevelCommand(BaseCommand):

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _execute(self) -> Iterable[SingleMessage]:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        keyboard = GroupsKeyboard(groups)
        return [SingleMessage(
            message="Выберите одну из групп",
            keyboard=keyboard
        )]
