from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

from app.data.database import Base
from app.data.enums import (
    RobotStatus, CommandStatus, AlertSeverity, AlertType, CommandType,
    ComponentStatus, ComponentDiagnosisState, ComponentType,
    ActionType, ActionStatus
)

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"
    __table_args__ = {'extend_existing': True}

    robot_id = Column(String, primary_key=True)
    name = Column(String)
    ip_address = Column(String)
    port = Column(Integer)
    version = Column(String)
    software_version = Column(String)
    capabilities = Column(JSON)
    status = Column(String, default=RobotStatus.OFFLINE.value)
    last_seen = Column(DateTime, default=datetime.utcnow)
    health_metrics = Column(JSON, nullable=True)
    current_location = Column(JSON, nullable=True)
    robot_metadata = Column(JSON, nullable=True)

    # Relationships
    commands = relationship("Command", back_populates="robot", cascade="all, delete-orphan")
    telemetry_data = relationship("TelemetryData", back_populates="robot", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="robot", cascade="all, delete-orphan")
    components = relationship("Component", back_populates="robot", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "robot_id": self.robot_id,
            "name": self.name,
            "ip_address": self.ip_address,
            "port": self.port,
            "version": self.version,
            "software_version": self.software_version,
            "capabilities": self.capabilities,
            "status": self.status,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "health_metrics": self.health_metrics,
            "current_location": self.current_location,
            "metadata": self.robot_metadata
        }

    @property
    def status_enum(self) -> RobotStatus:
        return RobotStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: RobotStatus):
        self.status = value.value

class Component(Base):
    __tablename__ = "components"
    __table_args__ = {'extend_existing': True}

    component_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    robot_id = Column(String, ForeignKey("robots.robot_id"))
    name = Column(String)
    component_type = Column(String, default=ComponentType.OTHER.value)
    status = Column(String, default=ComponentStatus.OPERATIONAL.value)
    diagnosis_state = Column(String, default=ComponentDiagnosisState.NORMAL.value)
    capabilities = Column(JSON)
    parameters = Column(JSON)
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    health_metrics = Column(JSON)
    component_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    robot = relationship("Robot", back_populates="components")
    actions = relationship("Action", back_populates="component", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "component_id": self.component_id,
            "robot_id": self.robot_id,
            "name": self.name,
            "component_type": self.component_type,
            "status": self.status,
            "diagnosis_state": self.diagnosis_state,
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
        return ComponentType(self.component_type)

    @component_type_enum.setter
    def component_type_enum(self, value: ComponentType):
        self.component_type = value.value

    @property
    def status_enum(self) -> ComponentStatus:
        return ComponentStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: ComponentStatus):
        self.status = value.value

    @property
    def diagnosis_state_enum(self) -> ComponentDiagnosisState:
        return ComponentDiagnosisState(self.diagnosis_state)

    @diagnosis_state_enum.setter
    def diagnosis_state_enum(self, value: ComponentDiagnosisState):
        self.diagnosis_state = value.value

class Action(Base):
    __tablename__ = "actions"
    __table_args__ = {'extend_existing': True}

    action_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    component_id = Column(String, ForeignKey("components.component_id"))
    name = Column(String)
    action_type = Column(String, default=ActionType.CUSTOM.value)
    status = Column(String, default=ActionStatus.PENDING.value)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    result = Column(JSON)
    error = Column(String)
    execution_time = Column(Float)

    # Relationships
    component = relationship("Component", back_populates="actions")
    steps = relationship("Step", back_populates="action", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "action_id": self.action_id,
            "component_id": self.component_id,
            "name": self.name,
            "action_type": self.action_type,
            "status": self.status,
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
        return ActionType(self.action_type)

    @action_type_enum.setter
    def action_type_enum(self, value: ActionType):
        self.action_type = value.value

    @property
    def status_enum(self) -> ActionStatus:
        return ActionStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: ActionStatus):
        self.status = value.value

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

    # Relationships
    action = relationship("Action", back_populates="steps")

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

class Command(Base):
    """Command model for storing robot commands"""
    __tablename__ = "commands"

    command_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    robot_id = Column(String(36), ForeignKey("robots.robot_id", ondelete="CASCADE"), nullable=False)
    command_type = Column(Enum(CommandType), nullable=False)
    status = Column(Enum(CommandStatus), nullable=False, default=CommandStatus.PENDING)
    parameters = Column(JSON, nullable=False, default=dict)
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    robot = relationship("Robot", back_populates="commands")

    def to_dict(self):
        return {
            "command_id": self.command_id,
            "robot_id": self.robot_id,
            "command_type": self.command_type.value,
            "status": self.status.value,
            "parameters": self.parameters,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @property
    def status_enum(self) -> CommandStatus:
        return CommandStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: CommandStatus):
        self.status = value.value

class TelemetryData(Base):
    __tablename__ = "telemetry_data"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    robot_id = Column(String, ForeignKey("robots.robot_id", ondelete="CASCADE"))
    timestamp = Column(DateTime)
    data = Column(JSON)

    robot = relationship("Robot", back_populates="telemetry_data")

class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    robot_id = Column(String, ForeignKey("robots.robot_id", ondelete="CASCADE"))
    type = Column(String)
    severity = Column(String, default=AlertSeverity.LOW.value)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON)

    robot = relationship("Robot", back_populates="alerts")

    @property
    def severity_enum(self) -> AlertSeverity:
        return AlertSeverity(self.severity)

    @severity_enum.setter
    def severity_enum(self, value: AlertSeverity):
        self.severity = value.value

    @property
    def type_enum(self) -> AlertType:
        return AlertType(self.type)

    @type_enum.setter
    def type_enum(self, value: AlertType):
        self.type = value.value 