from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

from app.api.action.model import Action
from app.api.component.model import RobotComponent
from app.api.step.model import RobotStep


class Robot(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the robot",
    )
    name: str = Field(..., description="Name of the robot")
    components: List[RobotComponent] = Field(
        default_factory=list,
        description="List of components that make up the robot",
    )
    actions: List[Action] = Field(
        default_factory=list,
        description="List of previous activities performed by the robot",
    )
    steps: List[RobotStep] = Field(
        default_factory=list,
        description="List of steps taken by the robot",
    )

    class Config:
        # Add this Config class to allow extra attributes
        extra = "ignore"
