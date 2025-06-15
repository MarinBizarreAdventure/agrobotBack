from typing import Optional, Dict, Any, List
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

# Import from data layer to avoid circular imports
from app.data.enums import ActionType, ActionStatus


class Action(BaseModel):
    action_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the action",
    )
    component_id: str
    name: str = Field(..., description="Name of the action")
    action_type: ActionType = Field(
        default=ActionType.CUSTOM,
        description="Type of action to be performed",
    )
    status: ActionStatus = Field(
        default=ActionStatus.PENDING,
        description="Current status of the action",
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for the action",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "action_id": "123e4567-e89b-12d3-a456-426614174000",
                "component_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Move to position",
                "action_type": "movement",
                "status": "pending",
                "parameters": {
                    "x": 10.0,
                    "y": 20.0,
                    "z": 0.0
                }
            }
        }
