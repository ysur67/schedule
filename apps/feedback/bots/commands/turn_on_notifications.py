from typing import Iterable

from apps.feedback.bots.commands.get_main_menu import get_main_menu_layout
from apps.feedback.bots.utils.keyboard.base import SimpleKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from asgiref.sync import sync_to_async

from .base import CommandWithProfile


class TurnOnNotificationsCommand(CommandWithProfile):

    async def _execute(self) -> Iterable[SingleMessage]:
        keyboard = SimpleKeyboard(data=get_main_menu_layout())
        if self.profile.send_notifications:
            return [SingleMessage(
                message="Ты уже получаешь уведомления!",
                keyboard=keyboard
            )]
        await sync_to_async(self.profile.toggle_notifications)(True)
        return [SingleMessage(
            message="Твои уведомления теперь включены!", keyboard=keyboard
        )]
