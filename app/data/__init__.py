from app.data.database import init_db, get_db
from app.data.models import Robot, Command, TelemetryData, Alert
from app.data.component.model import Component
from app.data.action.model import Action, Step

def get_robot_repository():
    from app.data.robot.repository import RobotRepository
    return RobotRepository

def get_component_repository():
    from app.data.component.repository import ComponentRepository
    return ComponentRepository

def get_action_repository():
    from app.data.action.repository import ActionRepository
    return ActionRepository

def get_step_repository():
    from app.data.step.repository import StepRepository
    return StepRepository

RobotRepository = property(get_robot_repository)
ComponentRepository = property(get_component_repository)
ActionRepository = property(get_action_repository)
StepRepository = property(get_step_repository)

__all__ = [
    "init_db",
    "get_db",
    "Robot",
    "Command",
    "TelemetryData",
    "Alert",
    "Component",
    "Action",
    "Step",
    "RobotRepository",
    "ComponentRepository",
    "ActionRepository",
    "StepRepository",
]
