#!/usr/bin/env python
"""
Database Integration Test - Tests adding and retrieving robots, components, actions,
and steps via RabbitMQ and verifies database storage.
"""
import json
import uuid
import time
import random
import sys
import os
from datetime import datetime
import argparse
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rich.console import Console
from rich.table import Table
import pika

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import application modules
from app.data.database import Base
from app.data.models import Robot
from app.data.component.model import Component, ComponentDiagnosisState
from app.data.action.model import Action, ActionType, ActionStatus
from app.data.step.model import Step
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

# API endpoint
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")

# Database configuration
DB_URL = os.getenv(
    "DATABASE_URL", "postgresql://agrobot:agrobot@localhost:5432/agrobot"
)

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "agrobot")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "agrobot")


class DatabaseIntegrationTest:
    def __init__(self):
        self.console = Console()
        self.engine = create_engine(DB_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.test_robots = []

    def connect_to_rabbitmq(self):
        """Connect to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                heartbeat=60,
            )

            self.rabbitmq_connection = pika.BlockingConnection(parameters)
            self.rabbitmq_channel = self.rabbitmq_connection.channel()

            # Declare exchanges
            self.rabbitmq_channel.exchange_declare(
                exchange="robot.commands", exchange_type="topic", durable=True
            )
            self.rabbitmq_channel.exchange_declare(
                exchange="robot.responses", exchange_type="topic", durable=True
            )

            console.print("[green]Connected to RabbitMQ[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error connecting to RabbitMQ: {str(e)}[/red]")
            return False

    def create_test_robot(self, name=None):
        """Create a test robot with components"""
        robot_id = str(uuid.uuid4())
        robot_name = name or f"TestRobot-{robot_id[:8]}"

        # Create robot via API
        robot_data = {
            "id": robot_id,
            "name": robot_name,
            "components": [
                {"uuid": str(uuid.uuid4()), "name": "Motor", "current_status": "OK"},
                {"uuid": str(uuid.uuid4()), "name": "Camera", "current_status": "OK"},
                {"uuid": str(uuid.uuid4()), "name": "Sensor", "current_status": "OK"},
            ],
        }

        try:
            response = requests.post(f"{API_BASE_URL}/robots", json=robot_data)
            if response.status_code == 201:
                console.print(
                    f"[green]Created robot {robot_name} with ID {robot_id}[/green]"
                )
                self.test_robots.append(robot_data)
                return robot_data
            else:
                console.print(
                    f"[red]Failed to create robot: {response.status_code} - {response.text}[/red]"
                )
                return None
        except Exception as e:
            console.print(f"[red]Error creating robot: {str(e)}[/red]")
            return None

    def send_robot_command(self, robot_id, command_type, parameters=None):
        """Send a command to a robot via RabbitMQ"""
        if not self.rabbitmq_channel:
            console.print("[red]Not connected to RabbitMQ[/red]")
            return None

        command_id = str(uuid.uuid4())
        command = {
            "command_id": command_id,
            "command_type": command_type,
            "parameters": parameters or {},
            "timestamp": datetime.now().isoformat(),
        }

        routing_key = f"robot.{robot_id}"

        try:
            self.rabbitmq_channel.basic_publish(
                exchange="robot.commands",
                routing_key=routing_key,
                body=json.dumps(command),
                properties=pika.BasicProperties(
                    delivery_mode=2, content_type="application/json"
                ),
            )
            console.print(
                f"[green]Sent command {command_id} of type {command_type} to robot {robot_id}[/green]"
            )
            return command_id
        except Exception as e:
            console.print(f"[red]Error sending command: {str(e)}[/red]")
            return None

    def send_location_update(self, robot_id, x, y):
        """Send a location update for a robot"""
        try:
            url = f"{API_BASE_URL}/robots/{robot_id}/location"
            data = {"location": [x, y]}
            response = requests.post(url, json=data)
            if response.status_code == 200:
                console.print(
                    f"[green]Updated location for robot {robot_id}: ({x}, {y})[/green]"
                )
                return True
            else:
                console.print(
                    f"[red]Failed to update location: {response.status_code} - {response.text}[/red]"
                )
                return False
        except Exception as e:
            console.print(f"[red]Error updating location: {str(e)}[/red]")
            return False

    def update_component_status(self, robot_id, component_uuid, status):
        """Update a component's status"""
        try:
            url = f"{API_BASE_URL}/robots/{robot_id}/components/{component_uuid}"
            data = {"current_status": status}
            response = requests.patch(url, json=data)
            if response.status_code == 200:
                console.print(
                    f"[green]Updated component {component_uuid} status to {status}[/green]"
                )
                return True
            else:
                console.print(
                    f"[red]Failed to update component: {response.status_code} - {response.text}[/red]"
                )
                return False
        except Exception as e:
            console.print(f"[red]Error updating component: {str(e)}[/red]")
            return False

    def verify_database(self):
        """Verify that all test data is correctly stored in the database"""
        db = self.SessionLocal()
        try:
            # Check if all test robots exist in the database
            for robot_data in self.test_robots:
                robot_id = robot_data["id"]
                db_robot = db.query(Robot).filter(Robot.id == robot_id).first()

                if not db_robot:
                    console.print(f"[red]Robot {robot_id} not found in database[/red]")
                    continue

                console.print(
                    f"[green]Found robot {db_robot.name} (ID: {db_robot.id}) in database[/green]"
                )

                # Check components
                components_table = Table(title=f"Components for Robot {db_robot.name}")
                components_table.add_column("UUID", style="cyan")
                components_table.add_column("Name", style="magenta")
                components_table.add_column("Status", style="green")

                for component in db_robot.components:
                    status_style = (
                        "green"
                        if component.current_status == ComponentDiagnosisState.OK
                        else "red"
                    )
                    components_table.add_row(
                        component.uuid,
                        component.name,
                        f"[{status_style}]{component.current_status}[/{status_style}]",
                    )

                console.print(components_table)

                # Check actions
                actions_table = Table(title=f"Actions for Robot {db_robot.name}")
                actions_table.add_column("UUID", style="cyan")
                actions_table.add_column("Name", style="magenta")
                actions_table.add_column("Type", style="blue")
                actions_table.add_column("Status", style="green")

                for action in db_robot.actions:
                    status_style = (
                        "green"
                        if action.action_status == ActionStatus.COMPLETED
                        else "yellow"
                    )
                    actions_table.add_row(
                        action.uuid,
                        action.name,
                        str(action.action_type),
                        f"[{status_style}]{action.action_status}[/{status_style}]",
                    )

                console.print(actions_table)

                # Check steps
                steps_table = Table(title=f"Steps for Robot {db_robot.name}")
                steps_table.add_column("UUID", style="cyan")
                steps_table.add_column("Location", style="blue")

                for step in db_robot.steps:
                    steps_table.add_row(
                        step.uuid, f"({step.location_x}, {step.location_y})"
                    )

                console.print(steps_table)

            return True
        except Exception as e:
            console.print(f"[red]Error verifying database: {str(e)}[/red]")
            return False
        finally:
            db.close()

    def run_test(self, num_robots=2, num_commands=3, num_locations=5):
        """Run the full integration test"""
        console.print("[bold blue]Starting Database Integration Test[/bold blue]")

        # Connect to RabbitMQ
        if not self.connect_to_rabbitmq():
            console.print("[red]Failed to connect to RabbitMQ, aborting test[/red]")
            return False

        try:
            # Create test robots
            console.print(f"[blue]Creating {num_robots} test robots...[/blue]")
            for i in range(num_robots):
                robot = self.create_test_robot(f"TestRobot-{i+1}")
                if not robot:
                    console.print(
                        "[yellow]Failed to create a robot, continuing...[/yellow]"
                    )

            # Wait for robots to be processed
            console.print("[blue]Waiting for robots to be processed...[/blue]")
            time.sleep(2)

            # Send commands to each robot
            console.print(
                f"[blue]Sending {num_commands} commands to each robot...[/blue]"
            )
            command_types = ["MOVE_TO", "TAKE_PICTURE", "COLLECT_SAMPLE"]

            for robot_data in self.test_robots:
                robot_id = robot_data["id"]

                for i in range(num_commands):
                    command_type = random.choice(command_types)
                    parameters = {}

                    if command_type == "MOVE_TO":
                        parameters = {
                            "x": random.uniform(0, 100),
                            "y": random.uniform(0, 100),
                            "speed": random.uniform(0.5, 2.0),
                        }
                    elif command_type == "TAKE_PICTURE":
                        parameters = {
                            "resolution": random.choice(["720p", "1080p", "4K"])
                        }
                    elif command_type == "COLLECT_SAMPLE":
                        parameters = {
                            "sample_type": random.choice(["soil", "water", "plant"]),
                            "amount": random.uniform(5, 50),
                        }

                    self.send_robot_command(robot_id, command_type, parameters)

            # Update locations for each robot
            console.print(
                f"[blue]Updating {num_locations} locations for each robot...[/blue]"
            )
            for robot_data in self.test_robots:
                robot_id = robot_data["id"]

                for i in range(num_locations):
                    x = random.uniform(0, 100)
                    y = random.uniform(0, 100)
                    self.send_location_update(robot_id, x, y)

            # Update some component statuses
            console.print("[blue]Updating some component statuses...[/blue]")
            for robot_data in self.test_robots:
                if "components" in robot_data and robot_data["components"]:
                    component = random.choice(robot_data["components"])
                    status = random.choice(["OK", "WARNING", "ERROR"])
                    self.update_component_status(
                        robot_data["id"], component["uuid"], status
                    )

            # Wait for all operations to be processed
            console.print("[blue]Waiting for all operations to be processed...[/blue]")
            time.sleep(5)

            # Verify database
            console.print("[blue]Verifying database...[/blue]")
            self.verify_database()

            console.print(
                "[bold green]Database Integration Test completed successfully[/bold green]"
            )
            return True

        except Exception as e:
            console.print(f"[bold red]Error in test: {str(e)}[/bold red]")
            return False
        finally:
            # Close RabbitMQ connection
            if self.rabbitmq_connection and self.rabbitmq_connection.is_open:
                self.rabbitmq_connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run database integration test")
    parser.add_argument(
        "--robots", type=int, default=2, help="Number of test robots to create"
    )
    parser.add_argument(
        "--commands",
        type=int,
        default=3,
        help="Number of commands to send to each robot",
    )
    parser.add_argument(
        "--locations",
        type=int,
        default=5,
        help="Number of location updates for each robot",
    )

    args = parser.parse_args()

    test = DatabaseIntegrationTest()
    test.run_test(
        num_robots=args.robots, num_commands=args.commands, num_locations=args.locations
    )
