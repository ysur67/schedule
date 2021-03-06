import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Type, TypeVar

from django.conf import settings

T = TypeVar("T", bound="BaseParser")


class BaseParser(ABC):
    url: str
    media_path: str
    logging_name: str

    @classmethod
    def build_parser(cls: Type[T], url: str) -> T:
        """Фабричный метод парсеров."""
        parser = cls(url)
        parser.set_up()
        return parser

    def __init__(self, url: str) -> None:
        self.url = url

    def set_up(self):
        self._set_up_logger()
        self.on_set_up()

    def on_set_up(self):
        """Дополнительный метод настройки, который будет вызван сразу после
        основной настройки парсера.

        Используйте его для дополнительной настройки парсера, вместо
        переопределения `set_up`.
        """
        pass

    @abstractmethod
    def parse(self):
        pass

    def _set_up_logger(self):
        self.logger = logging.getLogger(__name__)
        file_name = settings.LOGGING_DIR / self._build_logging_filename()
        file_handler = logging.FileHandler(str(file_name))
        self.logger.addHandler(file_handler)
        file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
        self.logger.setLevel(logging.DEBUG)

    def _build_logging_filename(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.logging_name} {current_time}.log"
