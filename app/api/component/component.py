import uuid
from pydantic import BaseModel, Field

from app.api.component.component_diagnosis_state import ComponentDiagnosisState


class RobotComponent(BaseModel):
    uuid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the robot component",
    )
    name: str = Field(..., description="Name of the robot component")
    current_status: ComponentDiagnosisState = Field(
        default=ComponentDiagnosisState.UNKNOWN,
        description="Current status of the robot component",
    )
