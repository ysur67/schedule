from typing import Iterable, Union

from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard.main_menu import MainMenuKeyboard
from asgiref.sync import sync_to_async

from .base import CommandWithProfile, SingleMessage


class TurnOnNotificationsCommand(CommandWithProfile):

    async def _execute(self) -> Iterable[SingleMessage]:
        keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        if self.profile.send_notifications:
            return [SingleMessage(
                message="Ты уже получаешь уведомления!",
                keyboard=keyboard
            )]
        await sync_to_async(self.profile.toggle_notifications)(True)
        return [SingleMessage(
            message="Твои уведомления теперь включены!", keyboard=keyboard
        )]
