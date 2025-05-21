from enum import Enum

# Import from data layer to avoid duplication and circular imports
from app.data.action.model import ActionType


class ActionType(str, Enum):
    AREA = "AREA"
    POINT = "POINT"
    PATH = "PATH"
