from .base import KeyboardMapper
from vkbottle import Keyboard


class ToVkKeyboardMapper(KeyboardMapper):

    def __init__(self, data: Keyboard) -> None:
        self.data = data

    def convert(self) -> str:
        return self.data.get_json()
