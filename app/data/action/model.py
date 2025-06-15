from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.data.database import Base
from app.data.enums import CommandStatus, ActionType, ActionStatus
from app.data.step.model import Step

class Action(Base):
    __tablename__ = "actions"
    __table_args__ = {'extend_existing': True}

    action_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    component_id = Column(String, ForeignKey("components.component_id"))
    name = Column(String)
    action_type = Column(String, default=ActionType.CUSTOM.value)  # Store as string
    status = Column(String, default=ActionStatus.PENDING.value)  # Store as string
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    result = Column(JSON)
    error = Column(String)
    execution_time = Column(Float)

    # Relationships with fully qualified paths
    component = relationship("app.data.component.model.Component", back_populates="actions")
    steps = relationship("app.data.step.model.Step", back_populates="action", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "action_id": self.action_id,
            "component_id": self.component_id,
            "name": self.name,
            "action_type": self.action_type,  # Already a string
            "status": self.status,  # Already a string
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "execution_time": self.execution_time
        }

    @property
    def action_type_enum(self) -> ActionType:
        """Get the action type as an enum value"""
        return ActionType(self.action_type)

    @action_type_enum.setter
    def action_type_enum(self, value: ActionType):
        """Set the action type from an enum value"""
        self.action_type = value.value

    @property
    def status_enum(self) -> ActionStatus:
        """Get the status as an enum value"""
        return ActionStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: ActionStatus):
        """Set the status from an enum value"""
        self.status = value.value
