from typing import Iterable

from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard import MainMenuKeyboard

from .base import BaseCommand, SingleMessage


class GetMainMenuCommand(BaseCommand):

    async def _execute(self) -> Iterable[SingleMessage]:
        keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        return [SingleMessage(
            message="Выберите один из пунктов меню",
            keyboard=keyboard
        )]
