from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.data.models import Robot
from app.data.enums import RobotStatus

logger = logging.getLogger(__name__)

class RobotRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Robot]:
        """Get all robots"""
        try:
            return self.session.query(Robot).all()
        except Exception as e:
            logger.error(f"Error getting all robots: {str(e)}")
            raise

    def get_by_id(self, robot_id: str) -> Optional[Robot]:
        """Get a robot by ID"""
        try:
            return self.session.query(Robot).filter(Robot.robot_id == robot_id).first()
        except Exception as e:
            logger.error(f"Error getting robot by ID: {str(e)}")
            raise

    def create(self, robot_data: Dict[str, Any]) -> Robot:
        """Create a new robot"""
        try:
            # Convert status enum to string if present
            if "status" in robot_data and isinstance(robot_data["status"], RobotStatus):
                robot_data["status"] = robot_data["status"].value

            robot = Robot(**robot_data)
            self.session.add(robot)
            self.session.commit()
            self.session.refresh(robot)
            return robot
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating robot: {str(e)}")
            raise

    def update(self, robot_id: str, robot_data: Dict[str, Any]) -> Optional[Robot]:
        """Update a robot"""
        try:
            robot = self.get_by_id(robot_id)
            if robot:
                # Convert status enum to string if present
                if "status" in robot_data and isinstance(robot_data["status"], RobotStatus):
                    robot_data["status"] = robot_data["status"].value

                for key, value in robot_data.items():
                    if key == "robot_metadata":
                        setattr(robot, "robot_metadata", value)
                    else:
                        setattr(robot, key, value)
                robot.last_seen = datetime.utcnow()
                self.session.commit()
                self.session.refresh(robot)
            return robot
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating robot: {str(e)}")
            raise

    def delete(self, robot_id: str) -> bool:
        """Delete a robot"""
        try:
            robot = self.get_by_id(robot_id)
            if robot:
                self.session.delete(robot)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting robot: {str(e)}")
            raise

    def update_status(self, robot_id: str, status: RobotStatus) -> Optional[Robot]:
        """Update robot status"""
        try:
            robot = self.get_by_id(robot_id)
            if robot:
                robot.status = status.value
                robot.last_seen = datetime.utcnow()
                self.session.commit()
                self.session.refresh(robot)
            return robot
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating robot status: {str(e)}")
            raise

    def get_by_ip(self, ip_address: str) -> Optional[Robot]:
        """Get a robot by IP address"""
        return self.session.query(Robot).filter(Robot.ip_address == ip_address).first()
