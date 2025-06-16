from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.data.enums import RobotStatus

class RobotCapability(BaseModel):
    name: str
    supported: bool
    details: Optional[Dict[str, Any]] = None

class RobotBaseDTO(BaseModel):
    """Base DTO for robot data"""
    name: str
    ip_address: str
    port: int
    version: str
    software_version: str
    capabilities: List[RobotCapability] = Field(default_factory=list)
    status: RobotStatus = RobotStatus.OFFLINE
    health_metrics: Optional[Dict[str, Any]] = None
    current_location: Optional[Dict[str, Any]] = None
    robot_metadata: Optional[Dict[str, Any]] = None

class RobotCreateDTO(RobotBaseDTO):
    """DTO for creating a robot"""
    robot_id: str

class RobotUpdateDTO(BaseModel):
    """DTO for updating a robot"""
    name: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    version: Optional[str] = None
    software_version: Optional[str] = None
    capabilities: Optional[List[RobotCapability]] = None
    status: Optional[RobotStatus] = None
    health_metrics: Optional[Dict[str, Any]] = None
    current_location: Optional[Dict[str, Any]] = None
    robot_metadata: Optional[Dict[str, Any]] = None

class RobotResponseDTO(RobotBaseDTO):
    """DTO for robot response"""
    robot_id: str
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True 