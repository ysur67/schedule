from typing import Iterable

from apps.feedback.bots.commands.utils import build_status_message
from apps.feedback.bots.utils.response.message import SingleMessage
from asgiref.sync import sync_to_async

from .base import CommandWithProfile


class GetCurrentStatusCommand(CommandWithProfile):

    async def _execute(self) -> Iterable[SingleMessage]:
        msg = await sync_to_async(build_status_message)(self.profile)
        return [SingleMessage(message=msg)]
