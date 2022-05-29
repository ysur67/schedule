from typing import Iterable, Union

from .base import BaseCommand, SingleMessage


class ShowIDCommand(BaseCommand):

    @property
    def user_id(self) -> str:
        return self._require_field("user_id")

    async def _execute(self) -> Iterable[SingleMessage]:
        return [
            SingleMessage("Привет!\nТвой идентификатор"),
            SingleMessage(str(self.user_id))
        ]
