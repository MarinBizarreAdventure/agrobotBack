# Don't import everything at module level to avoid circular imports
# Use lazy imports when needed

# Define what the module exports
__all__ = ["ComponentDiagnosisState", "RobotComponent", "ComponentService"]


# Lazy loading functions to avoid circular imports
def get_component_diagnosis_state():
    from app.data.component.model import ComponentDiagnosisState

    return ComponentDiagnosisState


def get_robot_component():
    from app.api.component.model import RobotComponent

    return RobotComponent


def get_component_service():
    from app.api.component.service import ComponentService

    return ComponentService


# Properties for lazy loading
ComponentDiagnosisState = property(get_component_diagnosis_state)  # type: ignore
RobotComponent = property(get_robot_component)  # type: ignore
ComponentService = property(get_component_service)  # type: ignore
