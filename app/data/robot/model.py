from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.data.database import Base


class Robot(Base):
    __tablename__ = "robots"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    components = relationship(
        "Component", back_populates="robot", cascade="all, delete-orphan"
    )
    actions = relationship(
        "Action", back_populates="robot", cascade="all, delete-orphan"
    )
    steps = relationship("Step", back_populates="robot", cascade="all, delete-orphan")

    def to_api_model(self):
        from app.api.robot.model import Robot as ApiRobot

        return ApiRobot(
            id=self.id,
            name=self.name,
            components=[component.to_api_model() for component in self.components],
            actions=[action.to_api_model() for action in self.actions],
            steps=[step.to_api_model() for step in self.steps],
        )

    @classmethod
    def from_api_model(cls, api_model):
        from app.data.component.model import Component
        from app.data.action.model import Action
        from app.data.step.model import Step

        robot = cls(id=api_model.id, name=api_model.name)

        if api_model.components:
            robot.components = [
                Component.from_api_model(component, robot.id)
                for component in api_model.components
            ]

        if api_model.actions:
            robot.actions = [
                Action.from_api_model(action, robot.id) for action in api_model.actions
            ]

        if api_model.steps:
            robot.steps = [
                Step.from_api_model(step, robot.id) for step in api_model.steps
            ]

        return robot
