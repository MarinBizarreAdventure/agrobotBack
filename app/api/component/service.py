from typing import List, Optional
from sqlalchemy.orm import Session

from app.api.component.model import RobotComponent
from app.data.component.repository import ComponentRepository


class ComponentService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.component_repo = ComponentRepository(db_session)

    def get_component(self, component_id: str) -> Optional[RobotComponent]:
        """Get a component by its ID"""
        component = self.component_repo.get_by_id(component_id)
        if component:
            return component.to_api_model()
        return None

    def list_components_by_robot(self, robot_id: str) -> List[RobotComponent]:
        """Get all components for a specific robot"""
        components = self.component_repo.list_by_robot(robot_id)
        return [component.to_api_model() for component in components]

    def create_component(
        self, component: RobotComponent, robot_id: str
    ) -> RobotComponent:
        """Create a new component for a robot"""
        from app.data.component.model import Component

        db_component = Component.from_api_model(component, robot_id)
        created_component = self.component_repo.create(db_component)
        return created_component.to_api_model()

    def update_component(self, component: RobotComponent) -> Optional[RobotComponent]:
        """Update an existing component"""
        existing = self.component_repo.get_by_id(component.uuid)
        if not existing:
            return None

        from app.data.component.model import Component

        # Preserve the robot_id when updating
        db_component = Component.from_api_model(component, existing.robot_id)
        updated_component = self.component_repo.update(db_component)
        return updated_component.to_api_model()

    def delete_component(self, component_id: str) -> bool:
        """Delete a component by its ID"""
        return self.component_repo.delete(component_id)
