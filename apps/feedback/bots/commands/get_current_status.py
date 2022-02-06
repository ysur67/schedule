from typing import Union

from asgiref.sync import sync_to_async

from apps.feedback.bots.commands.utils import build_status_message

from .base import CommandWithProfile, MultipleMessages, SingleMessage


class GetCurrentStatusCommand(CommandWithProfile):

    async def _execute_for_messengers(self) -> Union[SingleMessage, MultipleMessages]:
        msg = await sync_to_async(build_status_message)(self.profile)
        return SingleMessage(message=msg)
