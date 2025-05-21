from typing import List, Optional
from sqlalchemy.orm import Session

from app.data.robot.model import Robot


class RobotRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, robot_id: str) -> Optional[Robot]:
        """Get a robot by its ID"""
        return self.db_session.query(Robot).filter(Robot.id == robot_id).first()

    def list_all(self) -> List[Robot]:
        """Get all robots"""
        return self.db_session.query(Robot).all()

    def create(self, robot: Robot) -> Robot:
        """Create a new robot"""
        self.db_session.add(robot)
        self.db_session.commit()
        self.db_session.refresh(robot)
        return robot

    def update(self, robot: Robot) -> Robot:
        """Update an existing robot"""
        self.db_session.add(robot)
        self.db_session.commit()
        self.db_session.refresh(robot)
        return robot

    def delete(self, robot_id: str) -> bool:
        """Delete a robot by its ID"""
        robot = self.get_by_id(robot_id)
        if not robot:
            return False
        self.db_session.delete(robot)
        self.db_session.commit()
        return True
