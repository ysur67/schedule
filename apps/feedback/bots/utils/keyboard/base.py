from abc import ABC


class BaseKeyboard(ABC):

    def __init__(self) -> None:
        super().__init__()

    def to_api(self) -> str:
        return
