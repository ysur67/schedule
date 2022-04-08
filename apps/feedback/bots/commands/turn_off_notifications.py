from typing import Iterable, Union

from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard.main_menu import MainMenuKeyboard
from asgiref.sync import sync_to_async

from .base import CommandWithProfile, SingleMessage


class TurnOffNotificationsCommand(CommandWithProfile):

    async def _execute_for_messengers(self) -> Iterable[SingleMessage]:
        keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        if not self.profile.send_notifications:
            return [SingleMessage(
                message="У тебя уже и так отключены уведомления!",
                keyboard=keyboard
            )]
        await sync_to_async(self.profile.toggle_notifications)(False)
        return [SingleMessage(
            message="Больше ты не будешь получать уведомления!", keyboard=keyboard
        )]
