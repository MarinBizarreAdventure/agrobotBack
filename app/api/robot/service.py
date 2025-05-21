from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.api.robot.model import Robot as ApiRobot
from app.data.robot.repository import RobotRepository
from app.data.component.repository import ComponentRepository
from app.data.action.repository import ActionRepository
from app.data.step.repository import StepRepository
from app.messaging.service import MessagingService


class RobotService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.robot_repo = RobotRepository(db_session)
        self.component_repo = ComponentRepository(db_session)
        self.action_repo = ActionRepository(db_session)
        self.step_repo = StepRepository(db_session)
        self.messaging_service = None

    def set_messaging_service(self, messaging_service: MessagingService):
        """Set the messaging service for robot communication"""
        self.messaging_service = messaging_service

    def get_robot(self, robot_id: str) -> Optional[ApiRobot]:
        """Get a robot by its ID"""
        robot = self.robot_repo.get_by_id(robot_id)
        if robot:
            return robot.to_api_model()
        return None

    def list_robots(self) -> List[ApiRobot]:
        """Get all robots"""
        robots = self.robot_repo.list_all()
        return [robot.to_api_model() for robot in robots]

    def create_robot(self, robot: ApiRobot) -> ApiRobot:
        """Create a new robot"""
        from app.data.robot.model import Robot as DbRobot

        db_robot = DbRobot.from_api_model(robot)
        created_robot = self.robot_repo.create(db_robot)
        return created_robot.to_api_model()

    def update_robot(self, robot: ApiRobot) -> Optional[ApiRobot]:
        """Update an existing robot"""
        existing = self.robot_repo.get_by_id(robot.id)
        if not existing:
            return None

        from app.data.robot.model import Robot as DbRobot

        db_robot = DbRobot.from_api_model(robot)
        updated_robot = self.robot_repo.update(db_robot)
        return updated_robot.to_api_model()

    def delete_robot(self, robot_id: str) -> bool:
        """Delete a robot by its ID"""
        return self.robot_repo.delete(robot_id)

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
