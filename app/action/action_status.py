from enum import Enum


class ActionStatus(str, Enum):
    """
    Enum representing the status of an action.
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
