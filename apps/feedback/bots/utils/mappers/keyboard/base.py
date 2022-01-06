from abc import ABC
from typing import Any


class KeyboardMapper(ABC):

    def __init__(self, data: Any) -> None:
        self.data = data

    def convert(self) -> Any:
        pass
