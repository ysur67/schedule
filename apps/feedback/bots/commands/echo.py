from typing import Union

from vkbottle.tools.dev.mini_types.bot import message
from apps.feedback.bots.utils.const import Messengers
from .base import BaseCommand, MultipleMessages, SingleMessage


class HelloCommand(BaseCommand):

    @property
    def user_id(self) -> str:
        return self._require_field("user_id")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        return SingleMessage(message=f"Привет, {self.user_id}!")
