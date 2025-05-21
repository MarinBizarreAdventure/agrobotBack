from flask import Flask
from flasgger import Swagger
from rich import print as rprint
import os

# Environment configuration
from dotenv import load_dotenv

if os.environ.get("DOCKER_ENV") == "true":
    load_dotenv(".env.docker")
    rprint("[bold blue]Running in Docker environment[/bold blue]")
else:
    load_dotenv()
    rprint("[bold blue]Running in local environment[/bold blue]")

# Database
from app.data.database import init_db, SessionLocal

# Messaging service
from app.messaging.service import MessagingService

# Routers (Blueprints)
from app.router.command import command_router
from app.router.component import component_router
from app.router.health import health_router
from app.router.location import location_router
from app.router.robot import robot_router

# App
app = Flask(__name__)
swagger = Swagger(app)

# Register blueprints
app.register_blueprint(health_router)
app.register_blueprint(robot_router)
app.register_blueprint(location_router)
app.register_blueprint(command_router)
app.register_blueprint(component_router)

# Messaging service global
messaging_service = None


def main():
    """Main entry point for the application"""
    global messaging_service

    rprint("[bold green]Initializing Agrobot API...[/bold green]")

    # Initialize database
    init_db()
    rprint("[bold green]Database initialized.[/bold green]")

    # Initialize messaging service
    db_session = SessionLocal()
    messaging_service = MessagingService(db_session)
    messaging_service.start()

    # Stop messaging on exit
    import atexit

    atexit.register(lambda: messaging_service.stop())

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
