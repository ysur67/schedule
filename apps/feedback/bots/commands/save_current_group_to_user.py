from typing import Iterable, Union

from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard.main_menu import MainMenuKeyboard
from apps.timetables.usecases.group import get_group_by_title
from asgiref.sync import sync_to_async

from .base import CommandWithProfile, SingleMessage


class SaveCurrentGroupCommand(CommandWithProfile):

    @property
    def group(self) -> str:
        return self._require_field("group")

    async def _execute_for_messengers(self) -> Iterable[SingleMessage]:
        group = await sync_to_async(get_group_by_title)(self.group)
        await sync_to_async(self.profile.set_group)(group)
        keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        return [SingleMessage(
            message="Ваш выбор группы был успешно сохранен", keyboard=keyboard
        )]
