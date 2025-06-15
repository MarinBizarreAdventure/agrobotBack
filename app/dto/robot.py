from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RobotCapability(BaseModel):
    name: str
    supported: bool
    details: Optional[Dict[str, Any]] = None

class Location(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    timestamp: datetime

class Robot(BaseModel):
    robot_id: str
    name: str
    ip_address: str
    port: int
    version: str
    software_version: str
    capabilities: List[RobotCapability]
    status: str
    last_seen: Optional[datetime] = None
    health_metrics: Optional[Dict[str, Any]] = None
    current_location: Optional[Location] = None

    class Config:
        from_attributes = True

class RegisterRequest(BaseModel):
    robot_id: str
    robot_name: str
    version: str
    robot_ip_address: str
    robot_port: int
    capabilities: List[RobotCapability]
    location: Optional[Location] = None
    software_version: str
    metadata: Optional[Dict[str, Any]] = None

class RegisterResponse(BaseModel):
    success: bool
    message: str
    robot_config: Optional[Dict[str, Any]] = None

class QuickHealth(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    mavlink_connected: bool
    gps_fix: bool

class HeartbeatRequest(BaseModel):
    robot_id: str
    status: str
    timestamp: datetime
    quick_health: QuickHealth

class HeartbeatResponse(BaseModel):
    success: bool
    message: str
    commands_pending: bool

class GPSData(BaseModel):
    latitude: float
    longitude: float
    altitude: float

class AttitudeData(BaseModel):
    roll: float
    pitch: float
    yaw: float

class BatteryData(BaseModel):
    voltage: float
    current: float
    level: float

class SensorData(BaseModel):
    temperature: float
    pressure: float

class TelemetryData(BaseModel):
    timestamp: datetime
    gps: GPSData
    attitude: AttitudeData
    battery: BatteryData
    sensors: SensorData

class TelemetryBatchRequest(BaseModel):
    robot_id: str
    data: List[TelemetryData]

class TelemetryBatchResponse(BaseModel):
    success: bool
    message: str
    records_received: int

class CommandResultRequest(BaseModel):
    command_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

class CommandResultResponse(BaseModel):
    success: bool
    message: str

class AlertRequest(BaseModel):
    robot_id: str
    severity: str
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

class AlertResponse(BaseModel):
    success: bool
    message: str

class Command(BaseModel):
    command_id: str = Field(..., description="Unique identifier for the command")
    robot_id: str = Field(..., description="ID of the robot this command is for")
    command_type: str = Field(..., description="Type of command to execute")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for the command"
    )
    status: str = Field(
        default="pending",
        description="Current status of the command"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the command was created"
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="When the command was completed"
    )
    result: Optional[Dict[str, Any]] = Field(
        None,
        description="Result of the command execution"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if command failed"
    )
    execution_time: Optional[float] = Field(
        None,
        description="Time taken to execute the command in seconds"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "command_id": "123e4567-e89b-12d3-a456-426614174000",
                "robot_id": "123e4567-e89b-12d3-a456-426614174001",
                "command_type": "move_to_position",
                "parameters": {
                    "x": 10.0,
                    "y": 20.0,
                    "z": 0.0
                },
                "status": "pending"
            }
        }

class PollCommandsResponse(BaseModel):
    success: bool
    message: str
    commands: List[Command] 