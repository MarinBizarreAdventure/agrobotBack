from argparse import Action
from typing import List
from pydantic import BaseModel, Field
import uuid

from app.component.component import RobotComponent


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
    previous_activities: List[Action] = Field(
        default_factory=list,
        description="List of previous activities performed by the robot",
    )
