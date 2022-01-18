from typing import Union
from apps.feedback.bots.utils.const import MAIN_MENU_KEYBOARD_LAYOUT
from apps.feedback.bots.utils.keyboard.main_menu import MainMenuKeyboard
from .base import CommandWithProfile, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class TurnOnNotificationsCommand(CommandWithProfile):

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        _keyboard = MainMenuKeyboard(MAIN_MENU_KEYBOARD_LAYOUT)
        keyboard_data = _keyboard.to_vk_api()
        if self.profile.send_notifications:
            return SingleMessage(
                message="Ты уже получаешь уведомления!",
                keyboard=keyboard_data
            )
        await sync_to_async(self.profile.toggle_notifications)(True)
        return SingleMessage(
            message="Твои уведомления теперь включены!", keyboard=keyboard_data
        )
