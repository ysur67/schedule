from typing import Iterable

from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard.base import Button, SimpleKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage

from .base import BaseCommand


class GetMainMenuCommand(BaseCommand):

    async def _execute(self) -> Iterable[SingleMessage]:
        keyboard = SimpleKeyboard(
            data=get_main_menu_layout(),
            items_per_row=1,
            has_cancel_button=False
        )
        return [SingleMessage(
            message="Выберите один из пунктов меню",
            keyboard=keyboard
        )]


def get_main_menu_layout() -> 'list[Button]':
    return [Button(title=elem) for elem in MAIN_MENU_KEYBOARD_LAYOUT]
