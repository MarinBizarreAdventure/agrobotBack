from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.data.models import Command
from app.data.enums import CommandStatus, CommandType

logger = logging.getLogger(__name__)

class CommandRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Command]:
        try:
            return self.db.query(Command).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all commands: {str(e)}")
            raise

    def get_by_id(self, command_id: str) -> Optional[Command]:
        """Get a command by ID"""
        try:
            return self.db.query(Command).filter(Command.command_id == command_id).first()
        except Exception as e:
            logger.error(f"Error getting command by ID: {str(e)}")
            raise

    def get_pending_commands(self, robot_id: str) -> List[Command]:
        try:
            return self.db.query(Command).filter(
                Command.robot_id == robot_id,
                Command.status == CommandStatus.PENDING.value
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting pending commands for robot {robot_id}: {str(e)}")
            raise

    def get_pending_by_robot(self, robot_id: str) -> List[Command]:
        """Get pending commands for a robot"""
        try:
            return self.db.query(Command).filter(
                Command.robot_id == robot_id,
                Command.status == CommandStatus.PENDING
            ).all()
        except Exception as e:
            logger.error(f"Error getting pending commands: {str(e)}")
            raise

    def create(self, robot_id: str, command_type: CommandType, parameters: Dict[str, Any]) -> Command:
        """Create a new command"""
        try:
            command = Command(
                command_id=str(uuid.uuid4()),
                robot_id=robot_id,
                command_type=command_type,
                status=CommandStatus.PENDING,
                parameters=parameters
            )
            self.db.add(command)
            self.db.commit()
            self.db.refresh(command)
            return command
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating command: {str(e)}")
            raise

    def update(self, command_id: str, parameters: Dict[str, Any]) -> Optional[Command]:
        """Update a command"""
        try:
            command = self.get_by_id(command_id)
            if command:
                command.parameters = parameters
                command.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(command)
            return command
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating command: {str(e)}")
            raise

    def update_status(self, command_id: str, status: CommandStatus, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> Optional[Command]:
        """Update command status"""
        try:
            command = self.get_by_id(command_id)
            if command:
                command.status = status
                command.result = result
                command.error = error
                command.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(command)
            return command
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating command status: {str(e)}")
            raise

    def delete(self, command_id: str) -> bool:
        """Delete a command"""
        try:
            command = self.get_by_id(command_id)
            if command:
                self.db.delete(command)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting command: {str(e)}")
            raise 