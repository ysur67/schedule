from typing import Any, Iterable, List, Union
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from vkbottle.tools.dev.keyboard.color import KeyboardButtonColor

from apps.feedback.bots.utils.const import VK_MAX_BUTTONS_IN_KEYBOARD
from .base import BaseKeyboard
from vkbottle import Keyboard, Text
from apps.timetables.models import Group


class GroupsKeyboard(BaseKeyboard):

    def to_vk_api(self) -> Union[str, List[str]]:
        self.data: QuerySet[Group]
        if self.data.count() > VK_MAX_BUTTONS_IN_KEYBOARD:
            self.is_inline = True
            return self._build_multiple_keyboards(self.data)
        return self._build_single_keyboard(self.data)

    def _build_single_keyboard(self, groups: QuerySet[Group]) -> Keyboard:
        OFFSET = 2
        result = Keyboard(inline=self.is_inline)
        for index, value in enumerate(groups):
            result.add(Text(value.title))
            if (index + 1) % OFFSET == 0 and not self._is_last(index, groups):
                result.row()
        if self.has_cancel_button:
            result.row()
            result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()

    def _build_multiple_keyboards(self, groups: QuerySet[Group]) -> Iterable[Keyboard]:
        ITEMS_PER_PAGE = 8
        paginator = Paginator(groups.order_by("id"), ITEMS_PER_PAGE)
        result: List[str] = []
        for index in paginator.page_range:
            page = paginator.page(index)
            result.append(self._build_single_keyboard(page.object_list))
        return result