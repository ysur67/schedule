from typing import Iterable, Union
from apps.feedback.bots.commands.utils import build_status_message
from apps.feedback.bots.utils.keyboard.base import Button
from apps.feedback.bots.utils.keyboard.settings import SettingsKeyboard
from apps.feedback.models import Profile
from .base import CommandWithProfile, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class GetSettingsCommand(CommandWithProfile):

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        msg = await sync_to_async(build_status_message)(self.profile)
        layout: Iterable[Button] = await self.build_settings_keyboard_layout(self.profile)
        _keyboard = SettingsKeyboard(layout)
        keyboard = _keyboard.to_vk_api()
        return SingleMessage(
            message=msg,
            keyboard=keyboard
        )

    async def build_settings_keyboard_layout(self, profile: Profile) -> Iterable[Button]:
        if profile.send_notifications:
            toggle_notifications_title = "Отключить уведомления о занятиях"
        else:
            toggle_notifications_title = "Включить уведомления о занятиях"
        toggle_notifications_button = Button(title=toggle_notifications_title)
        change_group_button = Button(title="Выбрать группу")
        change_days_offset_value = Button(title="Изменить кол-во дней на расписание")
        return [
            toggle_notifications_button,
            change_group_button,
            change_days_offset_value,
        ]
