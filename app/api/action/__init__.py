# Import directly to avoid circular imports
from app.api.action.model import Action
from app.data.action.model import ActionStatus, ActionType


# Import service in a way that avoids circular imports
def get_action_service():
    from app.api.action.service import ActionService

    return ActionService()


# Create a property-like object for lazy loading
class LazyLoader:
    def __init__(self, load_func):
        self.load_func = load_func
        self.obj = None

    def __call__(self):
        if self.obj is None:
            self.obj = self.load_func()
        return self.obj


# Expose the service through lazy loading
ActionService = LazyLoader(get_action_service)

__all__ = ["Action", "ActionStatus", "ActionType", "ActionService"]
