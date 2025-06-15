from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.data.database import Base
from app.data.enums import RobotStatus, CommandStatus, AlertSeverity
from app.data.component.model import Component
from app.data.action.model import Action

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
    status = Column(String, default=RobotStatus.OFFLINE.value)  # Store as string
    last_seen = Column(DateTime, default=datetime.utcnow)
    health_metrics = Column(JSON, nullable=True)
    current_location = Column(JSON, nullable=True)
    robot_metadata = Column(JSON, nullable=True)

    # Relationships with fully qualified paths
    commands = relationship("app.data.models.Command", back_populates="robot", cascade="all, delete-orphan")
    telemetry_data = relationship("app.data.models.TelemetryData", back_populates="robot", cascade="all, delete-orphan")
    alerts = relationship("app.data.models.Alert", back_populates="robot", cascade="all, delete-orphan")
    components = relationship("app.data.component.model.Component", back_populates="robot", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "robot_id": self.robot_id,
            "name": self.name,
            "ip_address": self.ip_address,
            "port": self.port,
            "version": self.version,
            "software_version": self.software_version,
            "capabilities": self.capabilities,
            "status": self.status,  # Already a string
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "health_metrics": self.health_metrics,
            "current_location": self.current_location,
            "metadata": self.robot_metadata
        }

    @property
    def status_enum(self) -> RobotStatus:
        """Get the status as an enum value"""
        return RobotStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: RobotStatus):
        """Set the status from an enum value"""
        self.status = value.value

class Command(Base):
    __tablename__ = "commands"
    __table_args__ = {'extend_existing': True}

    command_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    robot_id = Column(String, ForeignKey("robots.robot_id"))
    command_type = Column(String)
    parameters = Column(JSON)
    status = Column(String, default=CommandStatus.PENDING.value)  # Store as string
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    result = Column(JSON)
    error = Column(String)
    execution_time = Column(Float)

    robot = relationship("app.data.models.Robot", back_populates="commands")

    @property
    def status_enum(self) -> CommandStatus:
        """Get the status as an enum value"""
        return CommandStatus(self.status)

    @status_enum.setter
    def status_enum(self, value: CommandStatus):
        """Set the status from an enum value"""
        self.status = value.value

class TelemetryData(Base):
    __tablename__ = "telemetry_data"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    robot_id = Column(String, ForeignKey("robots.robot_id"))
    timestamp = Column(DateTime)
    data = Column(JSON)  # Stores all telemetry data (GPS, attitude, battery, sensors)

    robot = relationship("app.data.models.Robot", back_populates="telemetry_data")

class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    robot_id = Column(String, ForeignKey("robots.robot_id"))
    severity = Column(String, default=AlertSeverity.INFO.value)  # Store as string
    message = Column(String)
    timestamp = Column(DateTime)
    details = Column(JSON)

    robot = relationship("app.data.models.Robot", back_populates="alerts")

    @property
    def severity_enum(self) -> AlertSeverity:
        """Get the severity as an enum value"""
        return AlertSeverity(self.severity)

    @severity_enum.setter
    def severity_enum(self, value: AlertSeverity):
        """Set the severity from an enum value"""
        self.severity = value.value 