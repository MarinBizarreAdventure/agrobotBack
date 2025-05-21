import uuid
from pydantic import BaseModel, Field

from app.action.action_status import ActionStatus
from app.action.action_type import ActionType


class Action(BaseModel):
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the action",
    )
    name: str = Field(..., description="Name of the action")
    action_type: ActionType = Field(
        default=ActionType.POINT,
        description="Type of action to be performed",
    )
    action_status: ActionStatus = Field(
        default=ActionStatus.PENDING,
        description="Current status of the action",
    )
