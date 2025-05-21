from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.data.database import Base


# Move the enum to avoid circular imports
class ComponentDiagnosisState(str, PyEnum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class Component(Base):
    __tablename__ = "components"

    uuid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    current_status = Column(
        Enum(ComponentDiagnosisState), default=ComponentDiagnosisState.UNKNOWN
    )
    robot_id = Column(String, ForeignKey("robots.id"))

    # Relationships
    robot = relationship("Robot", back_populates="components")

    def to_api_model(self):
        # Import here to avoid circular imports
        from app.api.component.model import RobotComponent

        return RobotComponent(
            uuid=self.uuid,
            name=self.name,
            current_status=self.current_status,
        )

    @classmethod
    def from_api_model(cls, api_model, robot_id=None):
        return cls(
            uuid=api_model.uuid,
            name=api_model.name,
            current_status=api_model.current_status,
            robot_id=robot_id,
        )
