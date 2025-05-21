import os
from sqlalchemy.orm import Session
from rich import print as rprint
from dotenv import load_dotenv

from app.messaging.mqtt.client import MQTTClient
from app.messaging.mqtt.handlers import MQTTMessageHandler
from app.messaging.rabbitmq.client import RabbitMQClient
from app.messaging.rabbitmq.handlers import RabbitMQMessageHandler

# Load environment variables from .env file
load_dotenv()


class MessagingService:
    """
    Orchestrates communication with robots via MQTT and RabbitMQ.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

        # Initialize MQTT client
        mqtt_host = os.getenv("MQTT_HOST", "localhost")
        mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
        self.mqtt_client = MQTTClient(broker_host=mqtt_host, broker_port=mqtt_port)
        self.mqtt_handler = MQTTMessageHandler(db_session)

        # Initialize RabbitMQ client with explicit credentials from environment
        rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        rabbitmq_port = int(os.getenv("RABBITMQ_PORT", "5672"))
        rabbitmq_user = os.getenv(
            "RABBITMQ_USER", "agrobot"
        )  # Default to "agrobot" instead of "guest"
        rabbitmq_pass = os.getenv(
            "RABBITMQ_PASS", "agrobot"
        )  # Default to "agrobot" instead of "guest"

        # Log the connection details (without the password)
        rprint(
            f"[blue]Connecting to RabbitMQ at {rabbitmq_host}:{rabbitmq_port} with user '{rabbitmq_user}'[/blue]"
        )

        self.rabbitmq_client = RabbitMQClient(
            host=rabbitmq_host,
            port=rabbitmq_port,
            username=rabbitmq_user,
            password=rabbitmq_pass,
        )
        self.rabbitmq_handler = RabbitMQMessageHandler(db_session)

    def start(self):
        """Start the messaging service"""
        rprint("[bold blue]Starting messaging service...[/bold blue]")

        # Set up MQTT subscriptions
        self.mqtt_client.subscribe(
            "robot/+/location", self.mqtt_handler.handle_location_update
        )
        self.mqtt_client.subscribe(
            "robot/+/component/status", self.mqtt_handler.handle_component_status
        )
        self.mqtt_client.subscribe(
            "robot/+/action/update", self.mqtt_handler.handle_action_update
        )

        # Set up RabbitMQ subscriptions
        # Queue for command responses
        self.rabbitmq_client.subscribe(
            "response.commands", self.rabbitmq_handler.handle_command_response
        )
        # Queue for telemetry data
        self.rabbitmq_client.subscribe(
            "telemetry.data", self.rabbitmq_handler.handle_telemetry_data
        )

        # Start clients
        self.mqtt_client.start()
        self.rabbitmq_client.start()

        rprint("[bold green]Messaging service started[/bold green]")

    def stop(self):
        """Stop the messaging service"""
        rprint("[bold blue]Stopping messaging service...[/bold blue]")

        self.mqtt_client.stop()
        self.rabbitmq_client.stop()

        rprint("[bold yellow]Messaging service stopped[/bold yellow]")

    def send_command_to_robot(self, robot_id: str, command: dict) -> bool:
        """Send a command to a robot using RabbitMQ"""
        return self.rabbitmq_client.send_command(robot_id, command)

    def publish_mqtt_message(self, topic: str, message: dict) -> None:
        """Publish a message to an MQTT topic"""
        self.mqtt_client.publish(topic, message)
