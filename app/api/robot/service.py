from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import json
import uuid
import logging

from app.data.robot.repository import RobotRepository
from app.data.models import Robot, Command, TelemetryData, Alert
from app.api.robot.dto import (
    Robot as ApiRobot,
    RegisterRequest,
    RegisterResponse,
    HeartbeatRequest,
    HeartbeatResponse,
    TelemetryBatchRequest,
    TelemetryBatchResponse,
    CommandResultRequest,
    CommandResultResponse,
    AlertRequest,
    AlertResponse,
    Command as ApiCommand,
    PollCommandsResponse
)
from app.data.component.repository import ComponentRepository
from app.data.action.repository import ActionRepository
from app.data.step.repository import StepRepository
from app.messaging.service import MessagingService
from app.utils.logger import logger
from app.data.enums import RobotStatus
from app.data.robot.dto import RobotCreateDTO, RobotUpdateDTO, RobotResponseDTO

logger = logging.getLogger(__name__)

class RobotService:
    def __init__(self, session: Session):
        self.repository = RobotRepository(session)
        self.component_repo = ComponentRepository(session)
        self.action_repo = ActionRepository(session)
        self.step_repo = StepRepository(session)
        self.messaging_service = None

    def set_messaging_service(self, service):
        """Set the messaging service for robot communication"""
        self.messaging_service = service

    def get_robot(self, robot_id: str) -> Optional[RobotResponseDTO]:
        """Get a robot by ID"""
        try:
            robot = self.repository.get_by_id(robot_id)
            if robot:
                # Parse capabilities from JSON string
                if isinstance(robot.capabilities, str):
                    robot.capabilities = json.loads(robot.capabilities)
                return RobotResponseDTO.from_orm(robot)
            return None
        except Exception as e:
            logger.error(f"Error getting robot: {str(e)}")
            raise

    def list_robots(self) -> List[RobotResponseDTO]:
        """Get all robots"""
        try:
            robots = self.repository.get_all()
            robot_dtos = []
            for robot in robots:
                # Parse capabilities from JSON string
                if isinstance(robot.capabilities, str):
                    robot.capabilities = json.loads(robot.capabilities)
                robot_dtos.append(RobotResponseDTO.from_orm(robot))
            return robot_dtos
        except Exception as e:
            logger.error(f"Error getting all robots: {str(e)}")
            raise

    def create_robot(self, robot_data: RobotCreateDTO) -> RobotResponseDTO:
        """Create a new robot"""
        try:
            robot = self.repository.create(robot_data.dict())
            return RobotResponseDTO.from_orm(robot)
        except Exception as e:
            logger.error(f"Error creating robot: {str(e)}")
            raise

    def update_robot(self, robot_id: str, robot_data: RobotUpdateDTO) -> Optional[RobotResponseDTO]:
        """Update a robot"""
        try:
            robot = self.repository.update(robot_id, robot_data.dict(exclude_unset=True))
            return RobotResponseDTO.from_orm(robot) if robot else None
        except Exception as e:
            logger.error(f"Error updating robot: {str(e)}")
            raise

    def delete_robot(self, robot_id: str) -> bool:
        """Delete a robot"""
        try:
            return self.repository.delete(robot_id)
        except Exception as e:
            logger.error(f"Error deleting robot: {str(e)}")
            raise

    def update_robot_status(self, robot_id: str, status: RobotStatus) -> Optional[RobotResponseDTO]:
        """Update robot status"""
        try:
            robot = self.repository.update_status(robot_id, status)
            return RobotResponseDTO.from_orm(robot) if robot else None
        except Exception as e:
            logger.error(f"Error updating robot status: {str(e)}")
            raise

    def send_command_to_robot(self, robot_id: str, command: Dict[str, Any]) -> bool:
        """Send a command to a robot"""
        if not self.messaging_service:
            logger.error("Messaging service not initialized")
            return False

        try:
            topic = f"robots/{robot_id}/commands"
            self.messaging_service.publish(topic, command)
            return True
        except Exception as e:
            logger.error(f"Error sending command to robot: {str(e)}")
            return False

    def get_latest_location(self, robot_id: str) -> Optional[tuple]:
        """Get the latest location for a robot"""
        steps = self.step_repo.list_by_robot(robot_id)
        if not steps:
            return None

        # Return the latest step's location
        latest_step = steps[-1]
        return (latest_step.location_x, latest_step.location_y)

    def register_robot(self, request: RegisterRequest) -> RegisterResponse:
        """Register a new robot or update an existing one"""
        try:
            # Convert capabilities to JSON string
            capabilities_json = json.dumps([cap.dict() for cap in request.capabilities])
            
            robot_data = {
                "robot_id": request.robot_id,
                "name": request.robot_name,
                "ip_address": request.robot_ip_address,
                "port": request.robot_port,
                "version": request.version,
                "software_version": request.software_version,
                "capabilities": capabilities_json,
                "current_location": request.location.dict() if request.location else None,
                "robot_metadata": request.metadata or {}
            }
            
            # Check if robot exists
            existing_robot = self.repository.get_by_id(request.robot_id)
            if existing_robot:
                # Update existing robot
                db_robot = self.repository.update(request.robot_id, robot_data)
                message = "Robot updated successfully"
            else:
                # Create new robot
                db_robot = self.repository.create(robot_data)
                message = "Robot registered successfully"
            
            return RegisterResponse(
                success=True,
                message=message,
                robot_id=db_robot.robot_id,
                robot_config={
                    "heartbeat_interval": 30,
                    "telemetry_interval": 60,
                    "mqtt_topics": {
                        "heartbeat": f"robots/{request.robot_id}/heartbeat",
                        "telemetry": f"robots/{request.robot_id}/telemetry",
                        "command_result": f"robots/{request.robot_id}/command_result",
                        "alert": f"robots/{request.robot_id}/alert"
                    }
                }
            )
        except Exception as e:
            logger.error(f"Error registering robot: {str(e)}")
            return RegisterResponse(
                success=False,
                message=f"Failed to register robot: {str(e)}",
                robot_id=request.robot_id if hasattr(request, 'robot_id') else None,
                robot_config={}
            )

    def process_heartbeat(self, heartbeat: HeartbeatRequest) -> HeartbeatResponse:
        """Process a robot heartbeat"""
        try:
            # Update robot status
            robot = self.repository.get_by_ip(heartbeat.robot_ip)
            if robot:
                # Update robot status and health metrics
                self.repository.update(robot.robot_id, {
                    "status": heartbeat.status,
                    "last_seen": heartbeat.timestamp,
                    "health_metrics": heartbeat.quick_health
                })
                
                # Check for pending commands
                has_pending = self._check_pending_commands(robot.robot_id)
                
                return HeartbeatResponse(
                    success=True,
                    message="Heartbeat received",
                    commands_pending=has_pending
                )
            return HeartbeatResponse(
                success=False,
                message="Robot not found",
                commands_pending=False
            )
        except Exception as e:
            logger.error(f"Error processing heartbeat: {str(e)}")
            return HeartbeatResponse(
                success=False,
                message=f"Error processing heartbeat: {str(e)}",
                commands_pending=False
            )

    def _check_pending_commands(self, robot_id: str) -> bool:
        """Check if there are any pending commands for the robot"""
        try:
            # Query the database for pending commands
            pending_commands = self.repository.session.query(Command).filter(
                Command.robot_id == robot_id,
                Command.status == CommandStatus.PENDING
            ).count()
            return pending_commands > 0
        except Exception as e:
            logger.error(f"Error checking pending commands: {str(e)}")
            return False

    def process_telemetry(self, request: TelemetryBatchRequest) -> TelemetryBatchResponse:
        robot = self.repository.get_by_id(request.robot_id)
        if not robot:
            return TelemetryBatchResponse(
                success=False,
                message="Robot not found",
                records_received=0
            )

        records = []
        for data in request.data:
            telemetry = TelemetryData(
                robot_id=request.robot_id,
                timestamp=data.timestamp,
                data=data.dict()
            )
            records.append(telemetry)

        self.repository.session.bulk_save_objects(records)
        self.repository.session.commit()

        return TelemetryBatchResponse(
            success=True,
            message="Telemetry data processed",
            records_received=len(records)
        )

    def process_command_result(self, request: CommandResultRequest) -> CommandResultResponse:
        command = self.repository.session.query(Command).filter(
            Command.command_id == request.command_id
        ).first()

        if not command:
            return CommandResultResponse(
                success=False,
                message="Command not found"
            )

        command.status = request.status
        command.result = request.result
        command.error = request.error
        command.execution_time = request.execution_time
        command.completed_at = datetime.utcnow()
        self.repository.session.commit()

        return CommandResultResponse(
            success=True,
            message="Command result processed"
        )

    def process_alert(self, request: AlertRequest) -> AlertResponse:
        robot = self.repository.get_by_id(request.robot_id)
        if not robot:
            return AlertResponse(
                success=False,
                message="Robot not found"
            )

        alert = Alert(
            robot_id=request.robot_id,
            severity=request.severity,
            message=request.message,
            timestamp=request.timestamp,
            details=request.details
        )
        self.repository.session.add(alert)
        self.repository.session.commit()

        return AlertResponse(
            success=True,
            message="Alert processed"
        )

    def get_pending_commands(self, robot_id: str) -> PollCommandsResponse:
        """Get pending commands for a robot"""
        try:
            # Get pending commands from database
            pending_commands = self.repository.session.query(Command).filter(
                Command.robot_id == robot_id,
                Command.status == CommandStatus.PENDING
            ).all()

            # Convert to response format
            commands = [
                Command(
                    command_id=cmd.command_id,
                    command_type=cmd.command_type,
                    parameters=cmd.parameters
                )
                for cmd in pending_commands
            ]

            return PollCommandsResponse(
                success=True,
                message="Pending commands retrieved",
                commands=commands
            )
        except Exception as e:
            logger.error(f"Error getting pending commands: {str(e)}")
            return PollCommandsResponse(
                success=False,
                message=f"Error getting pending commands: {str(e)}",
                commands=[]
            )
