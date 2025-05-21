from typing import Tuple
import uuid
from pydantic import BaseModel, Field


class RobotStep(BaseModel):
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the step",
    )
    location: Tuple[float, float] = Field(
        default=(0.0, 0.0),
        description="Coordinates of the step",
    )
