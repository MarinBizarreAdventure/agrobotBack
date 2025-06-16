from app.data.database import init_db, get_db
from app.data.models import (
    Robot,
    Command,
    TelemetryData,
    Alert,
    Component,
    Action,
    Step
)

# Repository imports
from app.data.robot.repository import RobotRepository
from app.data.component.repository import ComponentRepository
from app.data.action.repository import ActionRepository
from app.data.step.repository import StepRepository

def get_robot_repository():
    return RobotRepository()

def get_component_repository():
    return ComponentRepository()

def get_action_repository():
    return ActionRepository()

def get_step_repository():
    return StepRepository()

# Repository properties
RobotRepository = get_robot_repository
ComponentRepository = get_component_repository
ActionRepository = get_action_repository
StepRepository = get_step_repository

__all__ = [
    'init_db',
    'get_db',
    'Robot',
    'Command',
    'TelemetryData',
    'Alert',
    'Component',
    'Action',
    'Step',
    'RobotRepository',
    'ComponentRepository',
    'ActionRepository',
    'StepRepository'
]
