from typing import Optional, Dict, Any
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

from app.data.enums import ComponentStatus, ComponentDiagnosisState, ComponentType

class RobotComponent(BaseModel):
    component_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the robot component"
    )
    robot_id: str = Field(..., description="ID of the robot this component belongs to")
    name: str = Field(..., description="Name of the robot component")
    component_type: ComponentType = Field(
        default=ComponentType.CUSTOM,
        description="Type of the component"
    )
    status: ComponentStatus = Field(
        default=ComponentStatus.ACTIVE,
        description="Current status of the component"
    )
    diagnosis_state: ComponentDiagnosisState = Field(
        default=ComponentDiagnosisState.UNKNOWN,
        description="Current diagnosis state of the component"
    )
    capabilities: Dict[str, Any] = Field(
        default_factory=dict,
        description="Capabilities of the component"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for the component"
    )
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    health_metrics: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "component_id": "123e4567-e89b-12d3-a456-426614174000",
                "robot_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "GPS Module",
                "component_type": "gps",
                "status": "active",
                "diagnosis_state": "healthy",
                "capabilities": {
                    "accuracy": "0.5m",
                    "update_rate": "10Hz"
                },
                "parameters": {
                    "baud_rate": 9600,
                    "port": "/dev/ttyUSB0"
                }
            }
        }
