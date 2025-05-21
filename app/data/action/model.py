from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.data.database import Base


# Move enums to data layer to avoid circular imports
class ActionType(str, PyEnum):
    AREA = "AREA"
    POINT = "POINT"
    PATH = "PATH"


class ActionStatus(str, PyEnum):
    """
    Enum representing the status of an action.
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Action(Base):
    __tablename__ = "actions"

    uuid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    action_type = Column(Enum(ActionType), default=ActionType.POINT)
    action_status = Column(Enum(ActionStatus), default=ActionStatus.PENDING)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    robot_id = Column(String, ForeignKey("robots.id"))

    # Relationships
    robot = relationship("Robot", back_populates="actions")

    def to_api_model(self):
        # Import here to avoid circular imports
        from app.api.action.model import Action as ApiAction

        return ApiAction(
            uuid=self.uuid,
            name=self.name,
            action_type=self.action_type,
            action_status=self.action_status,
            start_time=self.start_time,
            end_time=self.end_time,
        )

    @classmethod
    def from_api_model(cls, api_model, robot_id=None):
        return cls(
            uuid=api_model.uuid,
            name=api_model.name,
            action_type=api_model.action_type,
            action_status=api_model.action_status,
            start_time=api_model.start_time,
            end_time=api_model.end_time,
            robot_id=robot_id,
        )
