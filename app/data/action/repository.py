from typing import List, Optional
from sqlalchemy.orm import Session

from app.data.action.model import Action


class ActionRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, action_id: str) -> Optional[Action]:
        """Get an action by its UUID"""
        return self.db_session.query(Action).filter(Action.uuid == action_id).first()

    def list_by_robot(self, robot_id: str) -> List[Action]:
        """Get all actions for a specific robot"""
        return self.db_session.query(Action).filter(Action.robot_id == robot_id).all()

    def create(self, action: Action) -> Action:
        """Create a new action"""
        self.db_session.add(action)
        self.db_session.commit()
        self.db_session.refresh(action)
        return action

    def update(self, action: Action) -> Action:
        """Update an existing action"""
        self.db_session.add(action)
        self.db_session.commit()
        self.db_session.refresh(action)
        return action

    def delete(self, action_id: str) -> bool:
        """Delete an action by its UUID"""
        action = self.get_by_id(action_id)
        if not action:
            return False
        self.db_session.delete(action)
        self.db_session.commit()
        return True
