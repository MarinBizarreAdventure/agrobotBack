from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator

from app.data.enums import CommandStatus, CommandType

class CommandBase(BaseModel):
    robot_id: str = Field(..., description="ID of the robot to execute the command")
    command_type: str = Field(..., description="Type of command to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Command parameters")

    @validator('command_type')
    def validate_command_type(cls, v):
        if v not in [cmd.value for cmd in CommandType]:
            raise ValueError(f"Invalid command type. Must be one of: {[cmd.value for cmd in CommandType]}")
        return v

class CommandCreate(CommandBase):
    pass

class CommandUpdate(BaseModel):
    status: Optional[CommandStatus] = None
    parameters: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class CommandResponse(CommandBase):
    command_id: str
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

    class Config:
        orm_mode = True

class CommandListResponse(BaseModel):
    commands: List[CommandResponse]
    total: int

class CommandErrorResponse(BaseModel):
    error: str
    details: Optional[Dict[str, Any]] = None

# Command-specific parameter models
class MoveCommandParameters(BaseModel):
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")
    z: float = Field(..., description="Z coordinate")
    speed: Optional[float] = Field(None, description="Movement speed")

class GotoCommandParameters(BaseModel):
    location_id: str = Field(..., description="ID of the target location")
    speed: Optional[float] = Field(None, description="Movement speed")

class SetModeCommandParameters(BaseModel):
    mode: str = Field(..., description="New robot mode")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Mode-specific parameters")

class MissionStep(BaseModel):
    command_type: str = Field(..., description="Type of command to execute")
    parameters: Dict[str, Any] = Field(..., description="Command parameters")
    sequence: int = Field(..., description="Step sequence number")

class CreateMissionCommandParameters(BaseModel):
    name: str = Field(..., description="Mission name")
    description: Optional[str] = Field(None, description="Mission description")
    steps: List[MissionStep] = Field(..., description="List of mission steps")
    priority: Optional[int] = Field(None, description="Mission priority") 