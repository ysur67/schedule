from typing import List
from bs4 import BeautifulSoup
from apps.exchange.parse import BaseHttpParser
from apps.timetables.models.group import EducationalLevel, Group
from apps.timetables.usecases.educational_level import create_educational_level, get_educational_level_by_title
import requests

from apps.timetables.usecases.group import create_group, get_group_by_title


class AllGroupsParser(BaseHttpParser):
    BASE_URL = "http://inet.ibi.spb.ru/raspisan/menu.php"
    logging_name = "All Groups"

    def parse(self):
        select = self.soup.find(id="ucstep")
        assert select, "select can't be None"
        for option in select.find_all("option"):
            level = self.parse_level(option)
            groups = self.parse_groups(level)

    def parse_level(self, item: BeautifulSoup) -> EducationalLevel:
        title = self.get_title(item)
        code = item.attrs.get("value", None)
        assert code, "code can't be None"
        level = get_educational_level_by_title(title)
        if not level:
            level = create_educational_level(title=title, code=code)
        return level

    def parse_groups(self, level: EducationalLevel) -> List[Group]:
        groups_soup = self.get_groups_by_request(level)
        result = []
        for group in groups_soup.find_all("option"):
            title = self.get_title(group)
            group = get_group_by_title(title)
            if not group:
                group = create_group(title=title, level=level)
            result.append(group)
        return result

    def get_groups_by_request(self, level: EducationalLevel) -> BeautifulSoup:
        url = self.BASE_URL + f"?tmenu={12}&cod={level.code}"
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
