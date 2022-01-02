from abc import ABC, abstractmethod


class BaseBot(ABC):

    def __init__(self, token: str) -> None:
        self.token = token

    @abstractmethod
    def listen(self) -> None:
        return
