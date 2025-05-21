from typing import List, Optional
from sqlalchemy.orm import Session

from app.data.component.model import Component


class ComponentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, component_id: str) -> Optional[Component]:
        """Get a component by its UUID"""
        return (
            self.db_session.query(Component)
            .filter(Component.uuid == component_id)
            .first()
        )

    def list_by_robot(self, robot_id: str) -> List[Component]:
        """Get all components for a specific robot"""
        return (
            self.db_session.query(Component)
            .filter(Component.robot_id == robot_id)
            .all()
        )

    def create(self, component: Component) -> Component:
        """Create a new component"""
        self.db_session.add(component)
        self.db_session.commit()
        self.db_session.refresh(component)
        return component

    def update(self, component: Component) -> Component:
        """Update an existing component"""
        self.db_session.add(component)
        self.db_session.commit()
        self.db_session.refresh(component)
        return component

    def delete(self, component_id: str) -> bool:
        """Delete a component by its UUID"""
        component = self.get_by_id(component_id)
        if not component:
            return False
        self.db_session.delete(component)
        self.db_session.commit()
        return True
