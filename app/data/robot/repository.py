from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.data.models import Robot
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RobotRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Robot]:
        """Get all robots"""
        try:
            return self.db.query(Robot).all()
        except Exception as e:
            logger.error(f"Error getting all robots: {str(e)}")
            raise

    def get_by_id(self, robot_id: str) -> Optional[Robot]:
        """Get a robot by its ID"""
        try:
            return self.db.query(Robot).filter(Robot.robot_id == robot_id).first()
        except Exception as e:
            logger.error(f"Error getting robot {robot_id}: {str(e)}")
            raise

    def create(self, robot_data: Dict[str, Any]) -> Robot:
        """Create or update a robot"""
        try:
            # Validate required fields
            required_fields = ["robot_id", "name", "ip_address", "port", "version", "software_version", "capabilities"]
            for field in required_fields:
                if field not in robot_data:
                    raise ValueError(f"Missing required field: {field}")

            # Check if robot already exists
            existing_robot = self.get_by_id(robot_data["robot_id"])
            if existing_robot:
                logger.info(f"Updating existing robot: {robot_data['robot_id']}")
                # Update existing robot
                for key, value in robot_data.items():
                    if key == "metadata":
                        setattr(existing_robot, "robot_metadata", value)
                    else:
                        setattr(existing_robot, key, value)
                existing_robot.last_seen = datetime.utcnow()
                self.db.commit()
                self.db.refresh(existing_robot)
                return existing_robot

            # Create new robot
            logger.info(f"Creating new robot: {robot_data['robot_id']}")
            db_robot = Robot(
                robot_id=robot_data["robot_id"],
                name=robot_data["name"],
                ip_address=robot_data["ip_address"],
                port=robot_data["port"],
                version=robot_data["version"],
                software_version=robot_data["software_version"],
                capabilities=robot_data["capabilities"],
                status="online",
                last_seen=datetime.utcnow(),
                health_metrics=robot_data.get("health_metrics"),
                current_location=robot_data.get("current_location"),
                robot_metadata=robot_data.get("metadata")
            )
            self.db.add(db_robot)
            self.db.commit()
            self.db.refresh(db_robot)
            return db_robot

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating/updating robot: {str(e)}")
            raise

    def update(self, robot_id: str, robot_data: Dict[str, Any]) -> Optional[Robot]:
        """Update a robot's data"""
        try:
            db_robot = self.get_by_id(robot_id)
            if db_robot:
                for key, value in robot_data.items():
                    if key == "metadata":
                        setattr(db_robot, "robot_metadata", value)
                    else:
                        setattr(db_robot, key, value)
                db_robot.last_seen = datetime.utcnow()
                self.db.commit()
                self.db.refresh(db_robot)
            return db_robot
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating robot {robot_id}: {str(e)}")
            raise

    def delete(self, robot_id: str) -> bool:
        """Delete a robot"""
        try:
            db_robot = self.get_by_id(robot_id)
            if db_robot:
                self.db.delete(db_robot)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting robot {robot_id}: {str(e)}")
            raise
