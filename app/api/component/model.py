from typing import Optional, Dict, Any, List
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

from app.data.enums import ComponentType, ComponentStatus, ComponentDiagnosisState

class RobotComponent(BaseModel):
    component_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the robot component"
    )
    robot_id: str = Field(..., description="ID of the robot this component belongs to")
    name: str = Field(..., description="Name of the robot component")
    component_type: str = Field(
        default=ComponentType.OTHER.value,
        description="Type of the component"
    )
    status: str = Field(
        default=ComponentStatus.OPERATIONAL.value,
        description="Current status of the component"
    )
    diagnosis_state: str = Field(
        default=ComponentDiagnosisState.NORMAL.value,
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
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the component"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the component was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the component was last updated"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "component_id": "123e4567-e89b-12d3-a456-426614174000",
                "robot_id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "GPS Module",
                "component_type": "gps",
                "status": "operational",
                "diagnosis_state": "normal",
                "capabilities": {
                    "accuracy": "0.5m",
                    "update_rate": "10Hz"
                },
                "parameters": {
                    "baud_rate": 9600,
                    "port": "/dev/ttyUSB0"
                },
                "last_maintenance": "2024-03-15T10:00:00Z",
                "next_maintenance": "2024-04-15T10:00:00Z",
                "metadata": {
                    "manufacturer": "AgroTech",
                    "model": "MT-2000",
                    "serial_number": "SN123456"
                }
            }
        }
