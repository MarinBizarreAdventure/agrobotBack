"""Router package for API routes."""

from app.router.health import health_router
from app.router.robot import robot_router
from app.router.component import component_router
from app.router.location import location_router
from app.router.command import command_router

__all__ = [
    "health_router",
    "robot_router",
    "component_router",
    "location_router",
    "command_router",
]
