from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from rich import print as rprint

from app.data.robot.repository import RobotRepository
from app.data.component.repository import ComponentRepository
from app.data.action.repository import ActionRepository
from app.data.step.repository import StepRepository
from app.data.component.model import ComponentDiagnosisState
from app.data.action.model import ActionStatus


class MQTTMessageHandler:
    """
    Handles MQTT messages from robots, processing and storing them in the database.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.robot_repo = RobotRepository(db_session)
        self.component_repo = ComponentRepository(db_session)
        self.action_repo = ActionRepository(db_session)
        self.step_repo = StepRepository(db_session)

    def handle_location_update(self, payload: Dict[str, Any]):
        """
        Handle location update messages from robots
        Expected payload: {"robot_id": "...", "location": [x, y], "timestamp": "..."}
        """
        try:
            robot_id = payload.get("robot_id")
            location = payload.get("location", [0, 0])

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

            step = RobotStep(location=(location[0], location[1]))
            db_step = Step.from_api_model(step, robot_id)

            self.step_repo.create(db_step)
            rprint(f"[green]Updated location for robot {robot_id}: {location}[/green]")

        except Exception as e:
            rprint(f"[bold red]Error handling location update: {str(e)}[/bold red]")

    def handle_component_status(self, payload: Dict[str, Any]):
        """
        Handle component status messages from robots
        Expected payload: {
            "robot_id": "...",
            "component_uuid": "...",
            "status": "OK|WARNING|ERROR|UNKNOWN",
            "details": "..."
        }
        """
        try:
            robot_id = payload.get("robot_id")
            component_uuid = payload.get("component_uuid")
            status = payload.get("status", "UNKNOWN")

            if not robot_id or not component_uuid:
                rprint(
                    "[bold red]Missing required fields in component status update[/bold red]"
                )
                return

            # Get the component
            component = self.component_repo.get_by_id(component_uuid)
            if not component:
                rprint(
                    f"[bold yellow]Component {component_uuid} not found[/bold yellow]"
                )
                return

            # Update component status
            try:
                component.current_status = ComponentDiagnosisState(status)
                self.component_repo.update(component)
                rprint(
                    f"[green]Updated status for component {component_uuid} to {status}[/green]"
                )
            except ValueError:
                rprint(f"[bold red]Invalid status value: {status}[/bold red]")

        except Exception as e:
            rprint(
                f"[bold red]Error handling component status update: {str(e)}[/bold red]"
            )

    def handle_action_update(self, payload: Dict[str, Any]):
        """
        Handle action update messages from robots
        Expected payload: {
            "robot_id": "...",
            "action_uuid": "...",
            "status": "PENDING|IN_PROGRESS|COMPLETED|FAILED",
            "timestamp": "..."
        }
        """
        try:
            robot_id = payload.get("robot_id")
            action_uuid = payload.get("action_uuid")
            status = payload.get("status")
            timestamp = payload.get("timestamp")

            if not robot_id or not action_uuid or not status:
                rprint("[bold red]Missing required fields in action update[/bold red]")
                return

            # Get the action
            action = self.action_repo.get_by_id(action_uuid)
            if not action:
                rprint(f"[bold yellow]Action {action_uuid} not found[/bold yellow]")
                return

            # Update action status
            try:
                action.action_status = ActionStatus(status)

                # Update timestamps based on status
                if status == ActionStatus.IN_PROGRESS and not action.start_time:
                    action.start_time = datetime.now()
                elif (
                    status in (ActionStatus.COMPLETED, ActionStatus.FAILED)
                    and not action.end_time
                ):
                    action.end_time = datetime.now()

                self.action_repo.update(action)
                rprint(
                    f"[green]Updated status for action {action_uuid} to {status}[/green]"
                )
            except ValueError:
                rprint(f"[bold red]Invalid action status: {status}[/bold red]")

        except Exception as e:
            rprint(f"[bold red]Error handling action update: {str(e)}[/bold red]")
