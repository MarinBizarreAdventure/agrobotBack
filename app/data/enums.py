from enum import Enum
from typing import Any


class CaseInsensitiveEnum(str, Enum):
    """Base class for case-insensitive enums"""
    @classmethod
    def _missing_(cls, value: Any) -> Any:
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None


class ActionType(CaseInsensitiveEnum):
    """Enum for action types"""
    CUSTOM = "custom"
    MOVEMENT = "movement"
    SENSOR_READING = "sensor_reading"
    CALIBRATION = "calibration"
    MAINTENANCE = "maintenance"
    DIAGNOSTIC = "diagnostic"


class ActionStatus(CaseInsensitiveEnum):
    """Enum for action status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ComponentDiagnosisState(CaseInsensitiveEnum):
    """Enum for component diagnosis states"""
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"


class RobotStatus(CaseInsensitiveEnum):
    """Enum for robot status"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class ComponentStatus(CaseInsensitiveEnum):
    """Enum for component status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class CommandStatus(CaseInsensitiveEnum):
    """Enum for command status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AlertSeverity(CaseInsensitiveEnum):
    """Enum for alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ComponentType(CaseInsensitiveEnum):
    """Enum for component types"""
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    CONTROLLER = "controller"
    CAMERA = "camera"
    GPS = "gps"
    BATTERY = "battery"
    MOTOR = "motor"
    CUSTOM = "custom" 