from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import json

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


class RobotService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = RobotRepository(db)
        self.component_repo = ComponentRepository(db)
        self.action_repo = ActionRepository(db)
        self.step_repo = StepRepository(db)
        self.messaging_service = None

    def set_messaging_service(self, messaging_service: MessagingService):
        """Set the messaging service for robot communication"""
        self.messaging_service = messaging_service

    def get_robot(self, robot_id: str) -> Optional[ApiRobot]:
        """Get a robot by its ID"""
        robot = self.repository.get_by_id(robot_id)
        if robot:
            return robot
        return None

    def list_robots(self) -> List[ApiRobot]:
        """Get all robots"""
        robots = self.repository.list_all()
        return robots

    def create_robot(self, robot: ApiRobot) -> ApiRobot:
        """Create a new robot"""
        db_robot = self.repository.create(robot)
        return db_robot

    def update_robot(self, robot: ApiRobot) -> Optional[ApiRobot]:
        """Update an existing robot"""
        existing = self.repository.get_by_id(robot.robot_id)
        if not existing:
            return None

        updated_robot = self.repository.update(robot)
        return updated_robot

    def delete_robot(self, robot_id: str) -> bool:
        """Delete a robot by its ID"""
        return self.repository.delete(robot_id)

    def send_command_to_robot(self, robot_id: str, command: Dict[str, Any]) -> bool:
        """Send a command to a robot"""
        if self.messaging_service is None:
            raise RuntimeError("Messaging service not initialized")

        return self.messaging_service.send_command_to_robot(robot_id, command)

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
            robot_data = {
                "robot_id": request.robot_id,
                "name": request.robot_name,
                "ip_address": request.robot_ip_address,
                "port": request.robot_port,
                "version": request.version,
                "software_version": request.software_version,
                "capabilities": [cap.dict() for cap in request.capabilities],
                "current_location": request.location.dict() if request.location else None,
                "robot_metadata": request.metadata
            }
            
            db_robot = self.repository.create(robot_data)
            
            return RegisterResponse(
                success=True,
                message="Robot registered successfully",
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
            return RegisterResponse(
                success=False,
                message=f"Failed to register robot: {str(e)}",
                robot_id=request.robot_id if hasattr(request, 'robot_id') else None,
                robot_config=None
            )

    def process_heartbeat(self, request: HeartbeatRequest) -> HeartbeatResponse:
        robot = self.repository.get_by_id(request.robot_id)
        if not robot:
            return HeartbeatResponse(
                success=False,
                message="Robot not found",
                commands_pending=False
            )

        robot_data = {
            "status": request.status,
            "last_seen": request.timestamp,
            "health_metrics": request.quick_health.dict()
        }
        self.repository.update(request.robot_id, robot_data)

        # Check for pending commands
        pending_commands = self.db.query(Command).filter(
            Command.robot_id == request.robot_id,
            Command.status == "pending"
        ).first()

        return HeartbeatResponse(
            success=True,
            message="Heartbeat processed",
            commands_pending=bool(pending_commands)
        )

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

        self.db.bulk_save_objects(records)
        self.db.commit()

        return TelemetryBatchResponse(
            success=True,
            message="Telemetry data processed",
            records_received=len(records)
        )

    def process_command_result(self, request: CommandResultRequest) -> CommandResultResponse:
        command = self.db.query(Command).filter(
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
        self.db.commit()

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
        self.db.add(alert)
        self.db.commit()

        return AlertResponse(
            success=True,
            message="Alert processed"
        )

    def get_pending_commands(self, robot_id: str) -> PollCommandsResponse:
        robot = self.repository.get_by_id(robot_id)
        if not robot:
            return PollCommandsResponse(
                success=False,
                message="Robot not found",
                commands=[]
            )

        pending_commands = self.db.query(Command).filter(
            Command.robot_id == robot_id,
            Command.status == "pending"
        ).all()

        commands = [
            ApiCommand(
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
