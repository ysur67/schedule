from apps.feedback.bots.utils.const import Messengers
from .base import BaseCommand


class HelloCommand(BaseCommand):

    @property
    def user_id(self) -> str:
        return self._require_field("user_id")

    async def _vk_execute(self) -> None:
        return [{
            "message": f"Привет, {self.user_id}!"
        }]
