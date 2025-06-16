from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.data.enums import CommandStatus, CommandType

class CommandBaseDTO(BaseModel):
    """Base DTO for command data"""
    robot_id: str
    command_type: CommandType
    parameters: Dict[str, Any] = Field(default_factory=dict)

class CommandCreateDTO(CommandBaseDTO):
    """DTO for creating a new command"""
    pass

class CommandUpdateDTO(BaseModel):
    """DTO for updating a command"""
    parameters: Dict[str, Any] = Field(default_factory=dict)

class CommandStatusUpdateDTO(BaseModel):
    """DTO for updating command status"""
    status: CommandStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class CommandResponseDTO(CommandBaseDTO):
    """DTO for command response"""
    command_id: str
    status: CommandStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 