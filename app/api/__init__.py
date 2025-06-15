# Import from modules directly for stable items, use lazy loading for services
from app.api.robot.dto import Robot
from app.api.component.model import RobotComponent
from app.data.component.model import ComponentDiagnosisState
from app.api.action.model import Action
from app.data.action.model import ActionStatus, ActionType
from app.api.step.model import RobotStep


# Lazy-load services to avoid circular imports
def get_robot_service():
    from app.api.robot.service import RobotService

    return RobotService


def get_component_service():
    from app.api.component.service import ComponentService

    return ComponentService


def get_action_service():
    from app.api.action.service import ActionService

    return ActionService


def get_step_service():
    from app.api.step.service import StepService

    return StepService


# Define services with lazy loading
RobotService = property(get_robot_service)
ComponentService = property(get_component_service)
ActionService = property(get_action_service)
StepService = property(get_step_service)

__all__ = [
    "Robot",
    "RobotService",
    "RobotComponent",
    "ComponentService",
    "ComponentDiagnosisState",
    "Action",
    "ActionService",
    "ActionStatus",
    "ActionType",
    "RobotStep",
    "StepService",
]
