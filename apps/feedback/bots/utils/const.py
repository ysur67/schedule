from enum import Enum


class Messengers(Enum):
    VK = "vk"
    TELEGRAM = "telegram"


class Commands(Enum):
    ECHO = "ECHO"
    GET_EDUCATIONAL_LEVELS = "GET_EDUCATIONAL_LEVELS"
    GET_GROUPS_BY_EDUCATIONAL_LEVEL = "GET_GROUPS_BY_EDUCATIONAL_LEVEL"


VK_MAX_BUTTONS_IN_KEYBOARD = 40
VK_MAX_ROWS_IN_KEYBOARD = 10


MAIN_MENU_KEYBOARD_LAYOUT = [
    "Показать расписание",
    "Выбор группы",
    "Настройки",
    "Статус",
]
assert len(MAIN_MENU_KEYBOARD_LAYOUT) <= VK_MAX_BUTTONS_IN_KEYBOARD, \
    f"Keyboards can't have more than {VK_MAX_BUTTONS_IN_KEYBOARD} buttons"
