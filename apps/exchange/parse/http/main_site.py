from .base import BaseHttpParser


class MainSiteParser(BaseHttpParser):
    logging_name: str = "Main Site Parser"

    def parse(self):
        pass
