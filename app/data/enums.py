from enum import Enum
from typing import Any


class CaseInsensitiveEnum(str, Enum):
    """Base class for case-insensitive enums"""
    @classmethod
    def _missing_(cls, value: Any) -> Any:
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return None


class ActionType(CaseInsensitiveEnum):
    """Enum for action types"""
    MOVE = "move"
    SCAN = "scan"
    COLLECT = "collect"
    ANALYZE = "analyze"
    REPORT = "report"
    CUSTOM = "custom"


class ActionStatus(CaseInsensitiveEnum):
    """Enum for action status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ComponentDiagnosisState(CaseInsensitiveEnum):
    """Enum for component diagnosis states"""
    NORMAL = "normal"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class RobotStatus(CaseInsensitiveEnum):
    """Enum for robot status"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    MAINTENANCE = "maintenance"


class ComponentStatus(CaseInsensitiveEnum):
    """Enum for component status"""
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    FAILED = "failed"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class CommandStatus(CaseInsensitiveEnum):
    """Enum for command status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CommandType(CaseInsensitiveEnum):
    """Enum for command types"""
    MOVE = "move"
    GOTO = "goto"
    ARM = "arm"
    DISARM = "disarm"
    SET_MODE = "set_mode"
    CREATE_MISSION = "create_mission"
    EXECUTE_MISSION = "execute_mission"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"
    CALIBRATE = "calibrate"
    UPDATE_FIRMWARE = "update_firmware"
    REBOOT = "reboot"
    SHUTDOWN = "shutdown"


class AlertSeverity(CaseInsensitiveEnum):
    """Enum for alert severity levels"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComponentType(CaseInsensitiveEnum):
    """Enum for component types"""
    MOTOR = "motor"
    SENSOR = "sensor"
    CAMERA = "camera"
    GPS = "gps"
    BATTERY = "battery"
    CONTROLLER = "controller"
    ACTUATOR = "actuator"
    OTHER = "other"


class StepStatus(CaseInsensitiveEnum):
    """Enum for step status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AlertType(CaseInsensitiveEnum):
    """Enum for alert type"""
    SYSTEM = "system"
    COMPONENT = "component"
    BATTERY = "battery"
    LOCATION = "location"
    STEP_FAILURE = "step_failure"
    COMMAND_FAILURE = "command_failure"
    OTHER = "other" 