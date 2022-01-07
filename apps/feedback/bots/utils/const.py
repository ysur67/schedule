from enum import Enum


class Messengers(Enum):
    VK = "VK"
    TELEGRAM = "TELGRAM"


class Commands(Enum):
    ECHO = "ECHO"
    GET_EDUCATIONAL_LEVELS = "GET_EDUCATIONAL_LEVELS"
    GET_GROUPS_BY_EDUCATIONAL_LEVEL = "GET_GROUPS_BY_EDUCATIONAL_LEVEL"
