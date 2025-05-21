from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.api.action.model import Action
from app.api.action.action_status import ActionStatus
from app.data.action.repository import ActionRepository


class ActionService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.action_repo = ActionRepository(db_session)

    def get_action(self, action_id: str) -> Optional[Action]:
        """Get an action by its ID"""
        action = self.action_repo.get_by_id(action_id)
        if action:
            return action.to_api_model()
        return None

    def list_actions_by_robot(self, robot_id: str) -> List[Action]:
        """Get all actions for a specific robot"""
        actions = self.action_repo.list_by_robot(robot_id)
        return [action.to_api_model() for action in actions]

    def create_action(self, action: Action, robot_id: str) -> Action:
        """Create a new action for a robot"""
        from app.data.action.model import Action as DbAction

        db_action = DbAction.from_api_model(action, robot_id)
        created_action = self.action_repo.create(db_action)
        return created_action.to_api_model()

    def update_action(self, action: Action) -> Optional[Action]:
        """Update an existing action"""
        existing = self.action_repo.get_by_id(action.uuid)
        if not existing:
            return None

        from app.data.action.model import Action as DbAction

        # Preserve the robot_id when updating
        db_action = DbAction.from_api_model(action, existing.robot_id)
        updated_action = self.action_repo.update(db_action)
        return updated_action.to_api_model()

    def start_action(self, action_id: str) -> Optional[Action]:
        """Start an action by setting its status to IN_PROGRESS and recording start time"""
        action = self.action_repo.get_by_id(action_id)
        if not action:
            return None

        action.action_status = ActionStatus.IN_PROGRESS
        action.start_time = datetime.now()

        updated_action = self.action_repo.update(action)
        return updated_action.to_api_model()

    def complete_action(self, action_id: str) -> Optional[Action]:
        """Complete an action by setting its status to COMPLETED and recording end time"""
        action = self.action_repo.get_by_id(action_id)
        if not action:
            return None

        action.action_status = ActionStatus.COMPLETED
        action.end_time = datetime.now()

        updated_action = self.action_repo.update(action)
        return updated_action.to_api_model()

    def fail_action(self, action_id: str) -> Optional[Action]:
        """Mark an action as failed and record end time"""
        action = self.action_repo.get_by_id(action_id)
        if not action:
            return None

        action.action_status = ActionStatus.FAILED
        action.end_time = datetime.now()

        updated_action = self.action_repo.update(action)
        return updated_action.to_api_model()

    def delete_action(self, action_id: str) -> bool:
        """Delete an action by its ID"""
        return self.action_repo.delete(action_id)
