from app.data.models import Robot

def get_robot_repository():
    from app.data.robot.repository import RobotRepository
    return RobotRepository

RobotRepository = property(get_robot_repository)

__all__ = ["Robot", "RobotRepository"]
