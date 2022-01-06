from apps.feedback.bots.utils.keyboard.base import BaseKeyboard
from .base import KeyboardMapper
from vkbottle import Keyboard


class ToVkKeyboardMapper(KeyboardMapper):

    def __init__(self, data: BaseKeyboard) -> None:
        self.data = data

    def convert(self) -> str:
        return self.data.result.get_json()
