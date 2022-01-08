from typing import Union
from apps.feedback.bots.commands.utils import build_status_message
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
        msg = await sync_to_async(build_status_message)(profile)
        return SingleMessage(message=msg)
