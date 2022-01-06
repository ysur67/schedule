from abc import ABC, abstractmethod
from vkbottle import Keyboard


class BaseKeyboard(ABC):
    result: Keyboard

    @classmethod
    def build_instance(cls) -> None:
        instance = cls()
        instance.init_keyboard()
        return instance

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def init_keyboard(self) -> Keyboard:
        pass

    def to_api(self) -> str:
        return self.result.get_json()
