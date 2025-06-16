from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from rich import print as rprint
import json
import logging

from app.data.robot.repository import RobotRepository
from app.data.component.repository import ComponentRepository
from app.data.action.repository import ActionRepository
from app.data.step.repository import StepRepository
from app.data.step.model import Step
from app.data.models import Alert
from app.data.enums import (
    ComponentDiagnosisState,
    ActionStatus,
    CommandStatus,
    StepStatus,
    AlertType,
    AlertSeverity
)
from app.data.database import get_db

logger = logging.getLogger(__name__)


class MQTTMessageHandler:
    """
    Handles MQTT messages from robots, processing and storing them in the database.
    """

    def __init__(
        self,
        robot_repository: RobotRepository,
        action_repository: ActionRepository,
        component_repository: Optional[ComponentRepository] = None,
        step_repository: Optional[StepRepository] = None
    ):
        self.robot_repo = robot_repository
        self.action_repo = action_repository
        self.component_repo = component_repository
        self.step_repo = step_repository

    def handle_location_update(self, payload: Dict[str, Any]):
        """
        Handle location update messages from robots
        Expected payload: {"robot_id": "...", "location": [x, y], "timestamp": "..."}
        """
        try:
            robot_id = payload.get("robot_id")
            location = payload.get("location", [0, 0])
            timestamp_str = payload.get("timestamp")

            # Parse timestamp if provided, otherwise use current time
            timestamp = None
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except ValueError:
                    rprint(
                        f"[yellow]Invalid timestamp format: {timestamp_str}, using current time instead[/yellow]"
                    )

            if timestamp is None:
                timestamp = datetime.now()

            if not robot_id:
                rprint("[bold red]Missing robot_id in location update[/bold red]")
                return

            # Check if robot exists
            robot = self.robot_repo.get_by_id(robot_id)
            if not robot:
                rprint(
                    f"[bold yellow]Robot {robot_id} not found, can't update location[/bold yellow]"
                )
                return

            # Create a new step entry for this location
            from app.api.step.model import RobotStep
            from app.data.step.model import Step

            step = RobotStep(location=(location[0], location[1]), timestamp=timestamp)
            db_step = Step.from_api_model(step, robot_id)

            if self.step_repo:
            self.step_repo.create(db_step)
            rprint(
                f"[green]Updated location for robot {robot_id}: {location} at {timestamp}[/green]"
            )
            else:
                rprint("Step repository not available, skipping location update")

        except Exception as e:
            rprint(f"[bold red]Error handling location update: {str(e)}[/bold red]")

    def handle_robot_status(self, robot_id: str, message: Dict[str, Any]) -> None:
        """Handle robot status updates"""
        try:
            status_data = {
                "status": message.get("status", "offline"),
                "last_seen": datetime.utcnow(),
                "health_metrics": message.get("health_metrics"),
                "current_location": message.get("location")
            }
            
            self.robot_repo.update(robot_id, status_data)
            logger.info(f"Updated status for robot {robot_id}")
            
        except Exception as e:
            logger.error(f"Error handling robot status for {robot_id}: {str(e)}")

    def handle_component_status(self, robot_id: str, message: Dict[str, Any]) -> None:
        """Handle component status updates"""
        if not self.component_repo:
            logger.warning("Component repository not available")
            return

        try:
            component_id = message.get("component_id")
            if not component_id:
                logger.error("No component_id in message")
                return

            status_data = {
                "status": message.get("status"),
                "diagnosis_state": message.get("diagnosis_state", ComponentDiagnosisState.UNKNOWN),
                "parameters": message.get("parameters", {}),
                "last_updated": datetime.utcnow()
            }

            self.component_repo.update(component_id, status_data)
            logger.info(f"Updated status for component {component_id}")
            
        except Exception as e:
            logger.error(f"Error handling component status: {str(e)}")

    def handle_action_status(self, robot_id: str, message: Dict[str, Any]) -> None:
        """Handle action status updates"""
        try:
            action_id = message.get("action_id")
            if not action_id:
                logger.error("No action_id in message")
                return

            status_data = {
                "status": message.get("status", ActionStatus.PENDING),
                "result": message.get("result"),
                "error": message.get("error"),
                "completed_at": datetime.utcnow() if message.get("status") == ActionStatus.COMPLETED else None
            }

            self.action_repo.update(action_id, status_data)
            logger.info(f"Updated status for action {action_id}")
            
        except Exception as e:
            logger.error(f"Error handling action status: {str(e)}")

    def handle_step_status(self, robot_id: str, message: Dict[str, Any]) -> None:
        """Handle step status updates"""
        if not self.step_repo:
            logger.warning("Step repository not available")
            return

        try:
            step_id = message.get("step_id")
            if not step_id:
                logger.error("No step_id in message")
                return

            status_data = {
                "status": message.get("status", CommandStatus.PENDING),
                "result": message.get("result"),
                "error": message.get("error"),
                "completed_at": datetime.utcnow() if message.get("status") == CommandStatus.COMPLETED else None
            }

            self.step_repo.update(step_id, status_data)
            logger.info(f"Updated status for step {step_id}")
            
        except Exception as e:
            logger.error(f"Error handling step status: {str(e)}")

    def handle_message(self, topic: str, payload: str) -> None:
        """Handle incoming MQTT messages"""
        try:
            # Extract robot_id from topic
            # Topic format: robots/{robot_id}/status
            parts = topic.split('/')
            if len(parts) < 3:
                logger.error(f"Invalid topic format: {topic}")
                return

            robot_id = parts[1]
            message_type = parts[2]
            message = json.loads(payload)

            # Route message to appropriate handler
            if message_type == "status":
                self.handle_robot_status(robot_id, message)
            elif message_type == "component":
                self.handle_component_status(robot_id, message)
            elif message_type == "action":
                self.handle_action_status(robot_id, message)
            elif message_type == "step":
                self.handle_step_status(robot_id, message)
            else:
                logger.warning(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON payload: {payload}")
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")

    def _handle_heartbeat(self, message: Dict[str, Any]) -> None:
        """
        Handle robot heartbeat message.
        """
        try:
            robot_id = message.get("robot_id")
            if not robot_id:
                logger.error("Heartbeat message missing robot_id")
                return

            # Update robot status
            with get_db() as db:
                self.robot_repo.update_status(
                    db, robot_id, "ONLINE", datetime.utcnow()
                )

        except Exception as e:
            logger.error(f"Error handling heartbeat: {str(e)}")

    def _handle_telemetry(self, message: Dict[str, Any]) -> None:
        """
        Handle robot telemetry message.
        """
        try:
            robot_id = message.get("robot_id")
            if not robot_id:
                logger.error("Telemetry message missing robot_id")
                return

            # Store telemetry data
            with get_db() as db:
                self.robot_repo.add_telemetry(
                    db,
                    robot_id,
                    message.get("location", {}),
                    message.get("battery_level"),
                    message.get("status"),
                    message.get("sensor_data", {}),
                )

        except Exception as e:
            logger.error(f"Error handling telemetry: {str(e)}")

    def _handle_command_result(self, message: Dict[str, Any]) -> None:
        """
        Handle robot command result message.
        """
        try:
            command_id = message.get("command_id")
            if not command_id:
                logger.error("Command result message missing command_id")
                return

            # Update command status
            with get_db() as db:
                self.action_repo.update_command_status(
                    db,
                    command_id,
                    message.get("status"),
                    message.get("result"),
                    message.get("error"),
                )

        except Exception as e:
            logger.error(f"Error handling command result: {str(e)}")

    def _handle_alert(self, message: Dict[str, Any]) -> None:
        """
        Handle robot alert message.
        """
        try:
            robot_id = message.get("robot_id")
            if not robot_id:
                logger.error("Alert message missing robot_id")
                return

            # Store alert
            with get_db() as db:
                self.robot_repo.add_alert(
                    db,
                    robot_id,
                    message.get("alert_type"),
                    message.get("message"),
                    message.get("severity"),
                    message.get("data", {}),
                )

        except Exception as e:
            logger.error(f"Error handling alert: {str(e)}")

    def handle_step_completion(self, message: Dict[str, Any]) -> None:
        """Handle step completion message."""
        try:
            step_id = message.get("step_id")
            status = message.get("status")
            result = message.get("result", {})
            
            if not step_id or not status:
                logger.error("Missing required fields in step completion message")
                return

            # Get the step from database
            db_step = self.step_repo.get_by_id(step_id)
            if not db_step:
                logger.error(f"Step {step_id} not found")
                return

            # Update step status
            db_step.status = status
            db_step.result = result
            db_step.completed_at = datetime.utcnow()
            
            # Save changes
            self.step_repo.update(db_step)
            
            # If step failed, create alert
            if status == StepStatus.FAILED.value:
                self._create_step_failure_alert(db_step, result)
            
            # Check if all steps are completed
            self._check_action_completion(db_step.action_id)

        except Exception as e:
            logger.error(f"Error handling step completion: {str(e)}")
            raise

    def _create_step_failure_alert(self, step: Step, result: Dict[str, Any]) -> None:
        """Create an alert for step failure."""
        try:
            alert = Alert(
                robot_id=step.robot_id,
                type=AlertType.STEP_FAILURE.value,
                severity=AlertSeverity.HIGH.value,
                message=f"Step {step.name} failed: {result.get('error', 'Unknown error')}",
                details={
                    "step_id": step.id,
                    "action_id": step.action_id,
                    "error": result.get("error"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            self.alert_repo.create(alert)
        except Exception as e:
            logger.error(f"Error creating step failure alert: {str(e)}")
            raise

    def _check_action_completion(self, action_id: str) -> None:
        """Check if all steps in an action are completed."""
        try:
            # Get all steps for this action
            steps = self.step_repo.get_by_action_id(action_id)
            if not steps:
                logger.warning(f"No steps found for action {action_id}")
                return
                
            # Check if all steps are completed
            all_completed = all(step.status == StepStatus.COMPLETED.value for step in steps)
            if all_completed:
                # Update action status
                self.action_repo.update(action_id, {
                    "status": ActionStatus.COMPLETED.value,
                    "completed_at": datetime.utcnow()
                })
                logger.info(f"Action {action_id} completed successfully")

        except Exception as e:
            logger.error(f"Error checking action completion: {str(e)}")
            raise
