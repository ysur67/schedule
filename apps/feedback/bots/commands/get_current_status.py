from typing import Iterable, Union

from apps.feedback.bots.commands.utils import build_status_message
from asgiref.sync import sync_to_async

from .base import CommandWithProfile, SingleMessage


class GetCurrentStatusCommand(CommandWithProfile):

    async def _execute_for_messengers(self) -> Iterable[SingleMessage]:
        msg = await sync_to_async(build_status_message)(self.profile)
        return [SingleMessage(message=msg)]
