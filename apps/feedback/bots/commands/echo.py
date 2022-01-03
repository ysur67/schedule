from .base import BaseCommand


class HelloCommand(BaseCommand):

    def __init__(self, user_id: str) -> None:
        super().__init__()
        self._id = user_id

    def execute(self) -> None:
        return f"Привет, {self._id}!"
