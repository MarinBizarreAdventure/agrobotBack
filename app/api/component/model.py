import uuid
from pydantic import BaseModel, Field

# Import from data layer to avoid circular imports
from app.data.component.model import ComponentDiagnosisState


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

    class Config:
        # Add this Config class for better validation
        use_enum_values = True
        extra = "ignore"
