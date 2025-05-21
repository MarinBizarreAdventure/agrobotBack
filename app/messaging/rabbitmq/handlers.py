from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from rich import print as rprint

from app.data.robot.repository import RobotRepository
from app.data.action.repository import ActionRepository
from app.data.action.model import ActionStatus


class RabbitMQMessageHandler:
    """
    Handles RabbitMQ messages from robots, processing command responses.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.robot_repo = RobotRepository(db_session)
        self.action_repo = ActionRepository(db_session)

    def handle_command_response(self, payload: Dict[str, Any]):
        """
        Handle command response messages from robots
        Expected payload: {
            "robot_id": "...",
            "command_id": "...",
            "status": "SUCCESS|FAILURE",
            "message": "...",
            "data": {...}
        }
        """
        try:
            robot_id = payload.get("robot_id")
            command_id = payload.get("command_id")
            status = payload.get("status")
            message = payload.get("message", "")

            if not robot_id or not command_id or not status:
                rprint(
                    "[bold red]Missing required fields in command response[/bold red]"
                )
                return

            rprint(
                f"[green]Received command response from robot {robot_id}: {status}[/green]"
            )
            rprint(f"[blue]Message: {message}[/blue]")

            # If the command was related to an action, update the action status
            action = self.action_repo.get_by_id(command_id)
            if action:
                if status == "SUCCESS":
                    action.action_status = ActionStatus.COMPLETED
                else:
                    action.action_status = ActionStatus.FAILED

                action.end_time = datetime.now()
                self.action_repo.update(action)
                rprint(
                    f"[green]Updated action {command_id} status to {action.action_status}[/green]"
                )

        except Exception as e:
            rprint(f"[bold red]Error handling command response: {str(e)}[/bold red]")

    def handle_telemetry_data(self, payload: Dict[str, Any]):
        """
        Handle telemetry data from robots
        Expected payload: {
            "robot_id": "...",
            "timestamp": "...",
            "data": {
                "battery": float,
                "cpu_usage": float,
                "memory_usage": float,
                "temperature": float,
                ...
            }
        }
        """
        # This would store telemetry data in a time-series database like InfluxDB
        # For now, we'll just log it
        try:
            robot_id = payload.get("robot_id")
            timestamp = payload.get("timestamp")
            data = payload.get("data", {})

            if not robot_id or not data:
                rprint("[bold red]Missing required fields in telemetry data[/bold red]")
                return

            rprint(f"[green]Received telemetry data from robot {robot_id}[/green]")
            rprint(f"[blue]Data: {data}[/blue]")

        except Exception as e:
            rprint(f"[bold red]Error handling telemetry data: {str(e)}[/bold red]")
