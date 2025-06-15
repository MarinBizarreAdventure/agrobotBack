from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.data.database import Base
from app.data.enums import CommandStatus

class Step(Base):
    __tablename__ = "steps"
    __table_args__ = {'extend_existing': True}

    step_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    action_id = Column(String, ForeignKey("actions.action_id"))
    sequence = Column(Integer)
    command = Column(String)
    parameters = Column(JSON)
    status = Column(Enum(CommandStatus), default=CommandStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    result = Column(JSON)
    error = Column(String)
    execution_time = Column(Float)

    # Relationships with fully qualified paths
    action = relationship("app.data.action.model.Action", back_populates="steps")

    def to_dict(self):
        return {
            "step_id": self.step_id,
            "action_id": self.action_id,
            "sequence": self.sequence,
            "command": self.command,
            "parameters": self.parameters,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "execution_time": self.execution_time
        }

    def to_api_model(self):
        from app.api.step.model import RobotStep

        return RobotStep(
            uuid=self.step_id,
            location=(self.location_x, self.location_y),
            timestamp=self.started_at,
        )

    @classmethod
    def from_api_model(cls, api_model, robot_id=None):
        return cls(
            step_id=api_model.uuid,
            action_id=api_model.action_id,
            step_type=api_model.step_type,
            status=api_model.status,
            parameters=api_model.parameters,
            result=api_model.result,
            error=api_model.error,
            started_at=api_model.started_at,
            completed_at=api_model.completed_at,
            location_x=api_model.location[0],
            location_y=api_model.location[1],
            robot_id=robot_id,
        )
