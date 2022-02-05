from typing import Union

from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard import MainMenuKeyboard

from .base import BaseCommand, MultipleMessages, SingleMessage


class GetMainMenuCommand(BaseCommand):

    async def _execute_for_messengers(self) -> Union[SingleMessage, MultipleMessages]:
        _keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        keyboard_data = _keyboard.to_vk_api()
        return SingleMessage(
            message="Выберите один из пунктов меню",
            keyboard=keyboard_data
        )
