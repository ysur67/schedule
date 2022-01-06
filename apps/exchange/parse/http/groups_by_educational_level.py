from typing import List
from bs4 import BeautifulSoup
from apps.timetables.models.group import EducationalLevel, Group
from apps.timetables.usecases.educational_level import create_educational_level, get_educational_level_by_title
from apps.timetables.usecases.group import create_group, get_group_by_title
from .base import BaseHttpParser


def has_selected_attribute(tag: BeautifulSoup) -> bool:
    return tag.has_attr("selected")


class GroupsByEducationalLevelsParser(BaseHttpParser):
    logging_name = "Groups Parser"

    def parse(self):
        level = self.parse_level()
        groups = self.parse_groups(level)

    def parse_level(self) -> EducationalLevel:
        # необходимо взять первый элемент, он будет говорить о том,
        # какой тип образования сейчас выбран
        selected = self.soup.find(has_selected_attribute)
        assert selected, "selected can't be None"
        title = self.get_title(selected)
        code = selected.attrs.get("value", None)
        assert code, "code can't be None"
        level = get_educational_level_by_title(title)
        if not level:
            level = create_educational_level(title=title, code=code)
        return level

    def parse_groups(self, level: EducationalLevel) -> List[Group]:
        select = self.soup.find(id="group")
        result = []
        for option in select.find_all("option"):
            title = self.get_title(option)
            group = get_group_by_title(title)
            if not group:
                group = create_group(title=title)
            group.level = level
            group.save()
            result.append(group)
        return result
