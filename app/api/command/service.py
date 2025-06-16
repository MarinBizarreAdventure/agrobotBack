from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.data.command.repository import CommandRepository
from app.data.models import Command
from app.data.enums import CommandStatus, CommandType
from app.api.command.dto import CommandCreate, CommandUpdate, CommandResponse
from app.data.command.dto import CommandCreateDTO, CommandUpdateDTO, CommandStatusUpdateDTO, CommandResponseDTO

logger = logging.getLogger(__name__)

class CommandService:
    def __init__(self, db: Session):
        self.repository = CommandRepository(db)

    def get_command(self, command_id: str) -> Optional[CommandResponseDTO]:
        """Get a command by ID"""
        command = self.repository.get_by_id(command_id)
        return CommandResponseDTO.from_orm(command) if command else None

    def get_pending_commands(self, robot_id: str) -> List[CommandResponseDTO]:
        """Get pending commands for a robot"""
        commands = self.repository.get_pending_by_robot(robot_id)
        return [CommandResponseDTO.from_orm(cmd) for cmd in commands]

    def create_command(self, command_data: CommandCreateDTO) -> CommandResponseDTO:
        """Create a new command"""
        command = self.repository.create(
            robot_id=command_data.robot_id,
            command_type=command_data.command_type,
            parameters=command_data.parameters
        )
        return CommandResponseDTO.from_orm(command)

    def update_command(self, command_id: str, command_data: CommandUpdateDTO) -> Optional[CommandResponseDTO]:
        """Update a command"""
        command = self.repository.get_by_id(command_id)
        if not command:
            return None
            
        command = self.repository.update(
            command_id=command_id,
            parameters=command_data.parameters
        )
        return CommandResponseDTO.from_orm(command) if command else None

    def update_command_status(self, command_id: str, status_data: CommandStatusUpdateDTO) -> Optional[CommandResponseDTO]:
        """Update command status"""
        command = self.repository.get_by_id(command_id)
        if not command:
            return None
            
        command = self.repository.update_status(
            command_id=command_id,
            status=status_data.status,
            result=status_data.result,
            error=status_data.error
        )
        return CommandResponseDTO.from_orm(command) if command else None

    def delete_command(self, command_id: str) -> bool:
        """Delete a command"""
        return self.repository.delete(command_id)

    def _validate_command_parameters(self, command_type: str, parameters: Dict[str, Any]) -> None:
        """Validate command parameters based on command type."""
        if command_type == CommandType.MOVE.value:
            required_params = ["x", "y", "z"]
            if not all(param in parameters for param in required_params):
                raise ValueError(f"Move command requires parameters: {required_params}")
            
        elif command_type == CommandType.GOTO.value:
            required_params = ["location_id"]
            if not all(param in parameters for param in required_params):
                raise ValueError(f"Goto command requires parameters: {required_params}")
            
        elif command_type == CommandType.SET_MODE.value:
            required_params = ["mode"]
            if not all(param in parameters for param in required_params):
                raise ValueError(f"Set mode command requires parameters: {required_params}")
            
        elif command_type == CommandType.CREATE_MISSION.value:
            required_params = ["name", "steps"]
            if not all(param in parameters for param in required_params):
                raise ValueError(f"Create mission command requires parameters: {required_params}")
            
            if not isinstance(parameters.get("steps"), list):
                raise ValueError("Mission steps must be a list") 