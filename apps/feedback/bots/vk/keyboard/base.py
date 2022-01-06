from abc import ABC


class BaseKeyboard(ABC):

    @classmethod
    def build_instance(cls) -> None:
        instance = cls()
        instance.init_keyboard()
        return instance

    def __init__(self) -> None:
        super().__init__()

    def init_keyboard(self) -> None:
        return

    def to_api(self) -> str:
        return
