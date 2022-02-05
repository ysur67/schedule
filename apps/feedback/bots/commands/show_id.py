from typing import Union

from .base import BaseCommand, MultipleMessages, SingleMessage


class ShowIDCommand(BaseCommand):

    @property
    def user_id(self) -> str:
        return self._require_field("user_id")

    async def _vk_execute(self) -> Union[SingleMessage, MultipleMessages]:
        return MultipleMessages([
            SingleMessage("Привет!\nТвой идентификатор"),
            SingleMessage(str(self.user_id))
        ])
