from typing import List, Optional
from sqlalchemy.orm import Session

from app.data.step.model import Step


class StepRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, step_id: str) -> Optional[Step]:
        """Get a step by its UUID"""
        return self.db_session.query(Step).filter(Step.uuid == step_id).first()

    def list_by_robot(self, robot_id: str) -> List[Step]:
        """Get all steps for a specific robot"""
        return self.db_session.query(Step).filter(Step.robot_id == robot_id).all()

    def create(self, step: Step) -> Step:
        """Create a new step"""
        self.db_session.add(step)
        self.db_session.commit()
        self.db_session.refresh(step)
        return step

    def update(self, step: Step) -> Step:
        """Update an existing step"""
        self.db_session.add(step)
        self.db_session.commit()
        self.db_session.refresh(step)
        return step

    def delete(self, step_id: str) -> bool:
        """Delete a step by its UUID"""
        step = self.get_by_id(step_id)
        if not step:
            return False
        self.db_session.delete(step)
        self.db_session.commit()
        return True
