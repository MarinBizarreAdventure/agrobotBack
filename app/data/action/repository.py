from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.data.action.model import Action
from app.data.enums import ActionStatus

logger = logging.getLogger(__name__)

class ActionRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> List[Action]:
        """Get all actions"""
        try:
            return self.db.query(Action).all()
        except Exception as e:
            logger.error(f"Error getting all actions: {str(e)}")
            return []

    def get_by_id(self, action_id: str) -> Optional[Action]:
        """Get action by ID"""
        try:
            return self.db.query(Action).filter(Action.action_id == action_id).first()
        except Exception as e:
            logger.error(f"Error getting action {action_id}: {str(e)}")
            return None

    def create(self, action_data: Dict[str, Any]) -> Optional[Action]:
        """Create a new action"""
        try:
            action = Action(**action_data)
            self.db.add(action)
            self.db.commit()
            self.db.refresh(action)
            return action
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating action: {str(e)}")
            return None

    def update(self, action_id: str, action_data: Dict[str, Any]) -> Optional[Action]:
        """Update an existing action"""
        try:
            action = self.get_by_id(action_id)
            if not action:
                return None

            for key, value in action_data.items():
                setattr(action, key, value)

            self.db.commit()
            self.db.refresh(action)
            return action
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating action {action_id}: {str(e)}")
            return None

    def delete(self, action_id: str) -> bool:
        """Delete an action"""
        try:
            action = self.get_by_id(action_id)
            if not action:
                return False

            self.db.delete(action)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting action {action_id}: {str(e)}")
            return False
