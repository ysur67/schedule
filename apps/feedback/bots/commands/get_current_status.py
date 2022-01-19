from typing import Union
from apps.feedback.bots.commands.utils import build_status_message
from .base import CommandWithProfile, MultipleMessages, SingleMessage
from asgiref.sync import sync_to_async


class GetCurrentStatusCommand(CommandWithProfile):

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        msg = await sync_to_async(build_status_message)(self.profile)
        return SingleMessage(message=msg)
