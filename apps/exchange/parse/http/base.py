from typing import Dict, Optional, Type, TypeVar
from ..base import BaseParser
import requests
from bs4 import BeautifulSoup
import enum


T = TypeVar("T", bound="BaseHttpParser")


class RequestType(enum.Enum):
    GET = "get"
    POST = "post"


class BaseHttpParser(BaseParser):
    request_type: RequestType

    @classmethod
    def build_parser(
        cls: Type[T],
        url: str,
        request_type: RequestType = RequestType.POST,
        payload_data: Dict = {}
        ) -> T:
        parser = cls(url, payload_data)
        parser.request_type = request_type
        parser.set_up()
        return parser

    def __init__(self, url: str, payload_data: Dict) -> None:
        super().__init__(url)
        self.payload_data = payload_data

    def on_set_up(self):
        if self.request_type == RequestType.POST:
            request = requests.post(self.url, data=self.payload_data)
        elif self.request_type == RequestType.GET:
            request = requests.get(self.url, data=self.payload_data)
        else:
            raise NotImplementedError(f"there is no approach for {self.request_type} method")
        if not request.ok:
            raise ValueError("код ответа не находится в промежутке 200-299")
        self.soup = BeautifulSoup(request.text, "html.parser")

    def get_title(self, item: BeautifulSoup, raise_exception: bool = True) -> Optional[str]:
        """Получить текст из блока BeautifulSoup

        Args:
            item (BeautifulSoup): Блок
            raise_exception (bool, optional): Флаг, указывающий на то, что
            необходимо поднимать исключение, если текста внутри блока нет.
            Defaults to True.
        """
        result = item.get_text().strip()
        if result:
            return result
        if raise_exception:
            raise ValueError("bs item has no title inside it")
        return None
