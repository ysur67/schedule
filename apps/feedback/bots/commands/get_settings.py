from typing import Iterable

from apps.feedback.bots.commands.utils import build_status_message
from apps.feedback.bots.utils.keyboard.base import Button
from apps.feedback.bots.utils.keyboard.settings import SettingsKeyboard
from apps.feedback.bots.utils.response.message import SingleMessage
from asgiref.sync import sync_to_async

from .base import CommandWithProfile


class GetSettingsCommand(CommandWithProfile):

    async def _execute(self) -> Iterable[SingleMessage]:
        msg = await sync_to_async(build_status_message)(self.profile)
        layout: Iterable[Button] = await self.build_settings_keyboard_layout()
        keyboard = SettingsKeyboard(layout)
        return [SingleMessage(
            message=msg,
            keyboard=keyboard
        )]

    async def build_settings_keyboard_layout(self) -> Iterable[Button]:
        change_group_button = Button(title="Выбрать группу")
        change_days_offset_value_button = Button(
            title="Изменить кол-во дней на расписание")
        show_my_id_button = Button(title="Покажи мой ID")
        return [
            change_group_button,
            change_days_offset_value_button,
            show_my_id_button
        ]
