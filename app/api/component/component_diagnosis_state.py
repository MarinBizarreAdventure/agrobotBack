# Import the enum from the data model to avoid duplication and circular imports
from app.data.component.model import ComponentDiagnosisState


class ComponentDiagnosisState(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"
