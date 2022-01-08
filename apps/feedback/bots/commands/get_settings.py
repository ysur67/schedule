from typing import Iterable, Union
from apps.feedback.bots.commands.utils import build_status_message
from apps.feedback.bots.utils.keyboard.base import Button
from apps.feedback.bots.utils.keyboard.settings import SettingsKeyboard
from apps.feedback.models import Profile
from apps.feedback.usecases.messenger import get_messenger_by_code
from apps.feedback.usecases.profile import get_profile_by_messenger_and_account_id
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class GetSettingsCommand(BaseCommand):

    @property
    def account_id(self) -> str:
        return self._require_field("account_id")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        messenger = await sync_to_async(get_messenger_by_code)(self.type.value)
        profile = await sync_to_async(get_profile_by_messenger_and_account_id)(messenger, self.account_id)
        msg = await sync_to_async(build_status_message)(profile)
        layout: Iterable[Button] = await self.build_settings_keyboard_layout(profile)
        _keyboard = SettingsKeyboard(layout)
        keyboard = _keyboard.to_vk_api()
        return SingleMessage(
            message=msg,
            keyboard=keyboard
        )

    async def build_settings_keyboard_layout(self, profile: Profile) -> Iterable[Button]:
        toggle_notifications_title = "❌ Отключить уведомления" if profile.send_notifications else "✅ Включить уведомления"
        toggle_notifications_button = Button(title=toggle_notifications_title)
        change_group_button = Button(title="Выбрать группу")
        return [
            toggle_notifications_button,
            change_group_button
        ]
