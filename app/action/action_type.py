from enum import Enum


class ActionType(str, Enum):
    AREA = "AREA"
    POINT = "POINT"
    PATH = "PATH"
