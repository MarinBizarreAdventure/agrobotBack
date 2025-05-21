from typing import List, Optional
from sqlalchemy.orm import Session

from app.api.step.model import RobotStep
from app.data.step.repository import StepRepository


class StepService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.step_repo = StepRepository(db_session)

    def get_step(self, step_id: str) -> Optional[RobotStep]:
        """Get a step by its ID"""
        step = self.step_repo.get_by_id(step_id)
        if step:
            return step.to_api_model()
        return None

    def list_steps_by_robot(self, robot_id: str) -> List[RobotStep]:
        """Get all steps for a specific robot"""
        steps = self.step_repo.list_by_robot(robot_id)
        return [step.to_api_model() for step in steps]

    def create_step(self, step: RobotStep, robot_id: str) -> RobotStep:
        """Create a new step for a robot"""
        from app.data.step.model import Step

        db_step = Step.from_api_model(step, robot_id)
        created_step = self.step_repo.create(db_step)
        return created_step.to_api_model()

    def update_step(self, step: RobotStep) -> Optional[RobotStep]:
        """Update an existing step"""
        existing = self.step_repo.get_by_id(step.uuid)
        if not existing:
            return None

        from app.data.step.model import Step

        # Preserve the robot_id when updating
        db_step = Step.from_api_model(step, existing.robot_id)
        updated_step = self.step_repo.update(db_step)
        return updated_step.to_api_model()

    def delete_step(self, step_id: str) -> bool:
        """Delete a step by its ID"""
        return self.step_repo.delete(step_id)
