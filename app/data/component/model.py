from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.data.database import Base
from app.data.enums import ComponentStatus, ComponentDiagnosisState, ComponentType
from app.data.action.model import Action

class Component(Base):
    __tablename__ = "components"
    __table_args__ = {'extend_existing': True}

    component_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    robot_id = Column(String, ForeignKey("robots.robot_id"))
    name = Column(String)
    component_type = Column(String, default=ComponentType.OTHER.value)  # Store as string
    status = Column(String, default=ComponentStatus.OPERATIONAL.value)  # Store as string
    diagnosis_state = Column(String, default=ComponentDiagnosisState.NORMAL.value)  # Store as string
    capabilities = Column(JSON)
    parameters = Column(JSON)
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    health_metrics = Column(JSON)
    component_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships with string references
    robot = relationship("Robot", back_populates="components")
    actions = relationship("Action", back_populates="component", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "component_id": self.component_id,
            "robot_id": self.robot_id,
            "name": self.name,
            "component_type": self.component_type,  # Already a string
            "status": self.status,  # Already a string
            "diagnosis_state": self.diagnosis_state,  # Already a string
            "capabilities": self.capabilities,
            "parameters": self.parameters,
            "last_maintenance": self.last_maintenance.isoformat() if self.last_maintenance else None,
            "next_maintenance": self.next_maintenance.isoformat() if self.next_maintenance else None,
            "health_metrics": self.health_metrics,
            "metadata": self.component_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @property
    def component_type_enum(self) -> ComponentType:
        """Get the component type as an enum value"""
        return ComponentType(self.component_type)

    @component_type_enum.setter
    def component_type_enum(self, value: ComponentType):
        """Set the component type from an enum value"""
        self.component_type = value.value

    @property
    def status_enum(self) -> ComponentStatus:
        """Get the status as an enum value"""
        return ComponentStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: ComponentStatus):
        """Set the status from an enum value"""
        self.status = value.value

    @property
    def diagnosis_state_enum(self) -> ComponentDiagnosisState:
        """Get the diagnosis state as an enum value"""
        return ComponentDiagnosisState(self.diagnosis_state)

    @diagnosis_state_enum.setter
    def diagnosis_state_enum(self, value: ComponentDiagnosisState):
        """Set the diagnosis state from an enum value"""
        self.diagnosis_state = value.value
