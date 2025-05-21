from enum import Enum

# Import from data layer to avoid duplication and circular imports
from app.data.action.model import ActionStatus


class ActionStatus(str, Enum):
    """
    Enum representing the status of an action.
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
