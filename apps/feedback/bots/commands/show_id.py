from typing import Iterable

from apps.feedback.bots.utils.response.message import SingleMessage

from .base import BaseCommand


class ShowIDCommand(BaseCommand):

    @property
    def user_id(self) -> str:
        return self._require_field("user_id")

    async def _execute(self) -> Iterable[SingleMessage]:
        return [
            SingleMessage("Привет!\nТвой идентификатор"),
            SingleMessage(str(self.user_id))
        ]
