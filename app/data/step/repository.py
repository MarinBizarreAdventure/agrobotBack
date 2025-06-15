from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.data.step.model import Step
from app.data.enums import CommandStatus

logger = logging.getLogger(__name__)

class StepRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> List[Step]:
        """Get all steps"""
        try:
            return self.db.query(Step).all()
        except Exception as e:
            logger.error(f"Error getting all steps: {str(e)}")
            return []

    def get_by_id(self, step_id: str) -> Optional[Step]:
        """Get step by ID"""
        try:
            return self.db.query(Step).filter(Step.step_id == step_id).first()
        except Exception as e:
            logger.error(f"Error getting step {step_id}: {str(e)}")
            return None

    def get_by_action_id(self, action_id: str) -> List[Step]:
        """Get all steps for an action"""
        try:
            return self.db.query(Step).filter(Step.action_id == action_id).order_by(Step.sequence).all()
        except Exception as e:
            logger.error(f"Error getting steps for action {action_id}: {str(e)}")
            return []

    def create(self, step_data: Dict[str, Any]) -> Optional[Step]:
        """Create a new step"""
        try:
            step = Step(**step_data)
            self.db.add(step)
            self.db.commit()
            self.db.refresh(step)
            return step
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating step: {str(e)}")
            return None

    def update(self, step_id: str, step_data: Dict[str, Any]) -> Optional[Step]:
        """Update an existing step"""
        try:
            step = self.get_by_id(step_id)
            if not step:
                return None

            for key, value in step_data.items():
                setattr(step, key, value)

            self.db.commit()
            self.db.refresh(step)
            return step
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating step {step_id}: {str(e)}")
            return None

    def delete(self, step_id: str) -> bool:
        """Delete a step"""
        try:
            step = self.get_by_id(step_id)
            if not step:
                return False

            self.db.delete(step)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting step {step_id}: {str(e)}")
            return False
