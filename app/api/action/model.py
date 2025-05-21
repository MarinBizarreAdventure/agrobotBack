from typing import Optional
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

# Import from data layer to avoid circular imports
from app.data.action.model import ActionStatus, ActionType


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
    start_time: Optional[datetime] = Field(
        default=None,
        description="Time when the action started",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="Time when the action ended",
    )
