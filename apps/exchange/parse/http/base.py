from typing import Dict, Type, TypeVar
from ..base import BaseParser
import requests
from bs4 import BeautifulSoup


T = TypeVar("T", bound="BaseHttpParser")

class BaseHttpParser(BaseParser):

    @classmethod
    def build_parser(cls: Type[T], url: str, payload_data: Dict) -> T:
        parser = cls(url, payload_data)
        parser.set_up()
        return parser

    def __init__(self, url: str, payload_data: Dict) -> None:
        super().__init__(url)
        self.payload_data = payload_data

    def on_set_up(self):
        request = requests.post(self.url, data=self.payload_data)
        self.soup = BeautifulSoup(request.text, "html.parser")
