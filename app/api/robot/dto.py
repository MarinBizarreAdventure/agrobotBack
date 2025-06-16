from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.data.enums import RobotStatus, CommandStatus, AlertSeverity

class RobotCapability(BaseModel):
    name: str
    supported: bool
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)

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
    status: str = Field(default=RobotStatus.OFFLINE.value)
    last_seen: Optional[datetime] = None
    health_metrics: Optional[Dict[str, Any]] = None
    current_location: Optional[Dict[str, Any]] = None
    robot_metadata: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
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
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RegisterResponse(BaseModel):
    success: bool
    message: str
    robot_id: str
    robot_config: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QuickHealth(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    mavlink_connected: bool
    gps_fix: bool

class HeartbeatRequest(BaseModel):
    robot_ip: str
    status: str
    timestamp: datetime
    quick_health: Dict[str, Any] = Field(default_factory=dict)

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
    gps: Dict[str, Any]
    attitude: Dict[str, Any]
    battery: Dict[str, Any]
    sensors: Dict[str, Any]

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
    details: Dict[str, Any] = Field(default_factory=dict)

class AlertResponse(BaseModel):
    success: bool
    message: str

class Command(BaseModel):
    command_id: str
    command_type: str
    parameters: Dict[str, Any]

class PollCommandsResponse(BaseModel):
    success: bool
    message: str
    commands: List[Command] 