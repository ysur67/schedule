from typing import Iterable

from apps.feedback.bots.utils.const import (VK_MAX_BUTTONS_IN_KEYBOARD,
                                            VK_MAX_ROWS_IN_KEYBOARD)
from apps.feedback.bots.utils.keyboard.base import Button, SimpleKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from apps.timetables.models import Group
from apps.timetables.usecases.educational_level import \
    get_educational_level_by_title
from apps.timetables.usecases.group import get_groups_by_educational_level
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import QuerySet

from .base import BaseCommand


class GetGroupsByLevelCommand(BaseCommand):
    BUTTONS_ON_SINGLE_KEYBOARD = 8

    @property
    def message(self) -> str:
        return self._require_field("message")

    async def _execute(self) -> Iterable[SingleMessage]:
        level = await sync_to_async(get_educational_level_by_title)(self.message)
        groups = get_groups_by_educational_level(level)
        count = await sync_to_async(groups.count)()
        rows = count / self.BUTTONS_ON_SINGLE_KEYBOARD
        if (count > VK_MAX_BUTTONS_IN_KEYBOARD) or (rows >= VK_MAX_ROWS_IN_KEYBOARD):
            response: 'list[SingleMessage]' = []
            response.append(SingleMessage('Выберите одну из групп'))
            keyboards = await sync_to_async(self._build_multiple_keyboards)(groups)
            for index, elem in enumerate(keyboards):
                response.append(SingleMessage(
                    message=str(index), keyboard=elem
                ))
            return response
        buttons = await sync_to_async(groups_to_buttons)(groups)
        keyboard = SimpleKeyboard(data=buttons)
        return [SingleMessage(
            message="Выберите одну из групп",
            keyboard=keyboard
        )]

    def _build_multiple_keyboards(self, groups: QuerySet[Group]) -> 'list[SingleMessage]':
        paginator = Paginator(
            groups.order_by("id"),
            self.BUTTONS_ON_SINGLE_KEYBOARD
        )
        result: 'list[SimpleKeyboard]' = []
        for index in paginator.page_range:
            page = paginator.page(index)
            result.append(
                SimpleKeyboard(
                    data=groups_to_buttons(page),
                    has_cancel_button=index == paginator.num_pages - 1,
                    is_inline=True,
                )
            )
        return result


def groups_to_buttons(groups: QuerySet[Group]) -> 'list[Button]':
    return [Button(title=item.title) for item in groups]
