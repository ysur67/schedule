import enum
from typing import Any, Iterable, List, Union

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from apps.feedback.bots.utils.const import (VK_MAX_BUTTONS_IN_KEYBOARD,
                                            VK_MAX_ROWS_IN_KEYBOARD)
from apps.timetables.models import Group
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from vkbottle import Keyboard, Text
from vkbottle.tools.dev.keyboard.color import KeyboardButtonColor


class GroupsKeyboard:
    OFFSET = 2
    ITEMS_PER_PAGE = 8

    def to_vk_api(self) -> Union[str, List[str]]:
        self.data: QuerySet[Group]
        count = self.data.count()
        rows = count / self.OFFSET
        if self.has_cancel_button:
            rows += 1
        if (count > VK_MAX_BUTTONS_IN_KEYBOARD) or (rows >= VK_MAX_ROWS_IN_KEYBOARD):
            self.is_inline = True
            return self._build_multiple_vk_keyboards(self.data)
        return self._build_single_vk_keyboard(self.data)

    def _build_single_vk_keyboard(self, groups: QuerySet[Group]) -> str:
        result = Keyboard(inline=self.is_inline)
        for index, value in enumerate(groups):
            result.add(Text(value.title))
            if ((index + 1) % self.OFFSET == 0) and not self._is_last(index, groups):
                result.row()
        if self.has_cancel_button:
            result.row()
            result.add(Text("Главное меню"), KeyboardButtonColor.PRIMARY)
        return result.get_json()

    def _build_multiple_vk_keyboards(self, groups: QuerySet[Group]) -> Iterable[str]:
        paginator = Paginator(groups.order_by("id"), self.ITEMS_PER_PAGE)
        result: List[str] = []
        self.has_cancel_button = False
        for index in paginator.page_range:
            page = paginator.page(index)
            result.append(self._build_single_vk_keyboard(page.object_list))
            if index == paginator.num_pages - 1:
                self.has_cancel_button = True
        return result

    def to_telegram_api(self) -> Union[ReplyKeyboardMarkup, List[InlineKeyboardMarkup]]:
        count = self.data.count()
        rows = count / self.OFFSET
        if self.has_cancel_button:
            rows += 1
        if (count > VK_MAX_BUTTONS_IN_KEYBOARD) or (rows >= VK_MAX_ROWS_IN_KEYBOARD):
            self.is_inline = True
            return self._build_multiple_telegram_keyboards()
        return self._build_single_telegram_keyboard(self.data)

    def _build_multiple_telegram_keyboards(self) -> List[InlineKeyboardMarkup]:
        paginator = Paginator(self.data.order_by("id"), self.ITEMS_PER_PAGE)
        result: List[InlineKeyboardMarkup] = []
        self.has_cancel_button = False
        for index in paginator.page_range:
            page = paginator.page(index)
            result.append(
                self._build_single_telegram_keyboard(page.object_list)
            )
            if index == paginator.num_pages - 1:
                self.has_cancel_button = True
        return result

    def _build_single_telegram_keyboard(self, groups: QuerySet[Group]) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        result = InlineKeyboardMarkup() if self.is_inline else ReplyKeyboardMarkup(
            resize_keyboard=True)
        result.row_width = self.OFFSET
        for index, value in enumerate(groups):
            title = value.title
            cancel_button = InlineKeyboardButton(
                title, callback_data=title) if self.is_inline else KeyboardButton(title)
            result.insert(cancel_button)
            if (((index + 1) % self.OFFSET) == 0) and not self._is_last(index, groups):
                result.row()
        if self.has_cancel_button:
            cancel_button = InlineKeyboardButton(
                'Главное меню', callback_data='Главное меню'
            ) if self.is_inline else KeyboardButton('Главное меню')
            result.add(cancel_button)
        return result
