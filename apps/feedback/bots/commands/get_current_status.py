from os import sync
from typing import Union
from apps.feedback.models import Profile
from apps.feedback.usecases.messenger import get_messenger_by_code
from apps.feedback.usecases.profile import get_profile_by_messenger_and_account_id
from .base import BaseCommand, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class GetCurrentStatusCommand(BaseCommand):

    @property
    def account_id(self) -> str:
        return self._require_field("account_id")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        messenger = await sync_to_async(get_messenger_by_code)(self.type.value)
        profile = await sync_to_async(get_profile_by_messenger_and_account_id)(messenger, self.account_id)
        msg = await self._build_message(profile)
        return SingleMessage(message=msg)

    async def _build_message(self, profile: Profile) -> str:
        group = await sync_to_async(profile.get_group)()
        result = f"Группа: {group.title}\n"
        send_notifications = "✅ Включены" if profile.send_notifications else "❌ Отключены"
        result += f"Уведомления: {send_notifications}\n"
        accounts_in_messengers = sync_to_async(list)(profile.get_accounts_in_messengers())
        for account in await accounts_in_messengers:
            messenger = await sync_to_async(account.get_messenger)()
            result += f"Имеется аккаунт в {messenger.title}\n"
        return result
