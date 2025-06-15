import os
import pika
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from rich import print as rprint
from dotenv import load_dotenv
from app.config import Config
import logging
from typing import Optional

from app.messaging.mqtt.client import MQTTClient
from app.messaging.mqtt.handlers import MQTTMessageHandler
from app.messaging.rabbitmq.client import RabbitMQClient
from app.messaging.rabbitmq.handlers import RabbitMQMessageHandler
from app.data.robot.repository import RobotRepository
from app.data.action.repository import ActionRepository
from app.data.component.repository import ComponentRepository
from app.data.step.repository import StepRepository
from app.data.database import get_db

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class MessagingService:
    """
    Orchestrates communication with robots via MQTT and RabbitMQ.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.mqtt_client: Optional[MQTTClient] = None
        self.rabbitmq_connection: Optional[pika.BlockingConnection] = None
        self.rabbitmq_channel: Optional[pika.channel.Channel] = None

    def start(self):
        """Start the messaging service."""
        try:
            self._setup_mqtt()
            self._setup_rabbitmq()
            logger.info("Messaging service started successfully")
        except Exception as e:
            logger.error(f"Failed to start messaging service: {str(e)}")
            raise

    def stop(self):
        """Stop the messaging service."""
        try:
            if self.mqtt_client:
                self.mqtt_client.disconnect()
            if self.rabbitmq_connection and not self.rabbitmq_connection.is_closed:
                self.rabbitmq_connection.close()
            logger.info("Messaging service stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping messaging service: {str(e)}")

    def _setup_rabbitmq(self):
        """Set up RabbitMQ connection and channels"""
        try:
            credentials = pika.PlainCredentials(
                Config.RABBITMQ_USER,
                Config.RABBITMQ_PASSWORD
            )
            parameters = pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                port=Config.RABBITMQ_PORT,
                credentials=credentials,
                virtual_host='/'  # Use default virtual host
            )
            self.rabbitmq_connection = pika.BlockingConnection(parameters)
            self.command_channel = self.rabbitmq_connection.channel()
            self.command_channel.queue_declare(queue='robot_commands')
            self.telemetry_channel = self.rabbitmq_connection.channel()
            self.telemetry_channel.queue_declare(queue='robot_telemetry')
            self.alert_channel = self.rabbitmq_connection.channel()
            self.alert_channel.queue_declare(queue='robot_alerts')
            logger.info("RabbitMQ connection established")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise

    def _setup_mqtt(self):
        """Set up MQTT client."""
        try:
            # Initialize repositories with the session
            robot_repository = RobotRepository(self.db_session)
            action_repository = ActionRepository(self.db_session)
            component_repository = ComponentRepository(self.db_session)
            step_repository = StepRepository(self.db_session)
            
            # Create message handler
            handler = MQTTMessageHandler(
                robot_repository=robot_repository,
                action_repository=action_repository,
                component_repository=component_repository,
                step_repository=step_repository
            )
            
            # Create and connect MQTT client
            self.mqtt_client = MQTTClient(
                broker_host=Config.MQTT_BROKER,
                broker_port=Config.MQTT_PORT
            )
            
            # Set up authentication if provided
            if Config.MQTT_USERNAME and Config.MQTT_PASSWORD:
                self.mqtt_client.client.username_pw_set(
                    Config.MQTT_USERNAME,
                    Config.MQTT_PASSWORD
                )
            
            # Subscribe to topics
            self.mqtt_client.subscribe("robots/+/heartbeat", handler.handle_message)
            self.mqtt_client.subscribe("robots/+/telemetry", handler.handle_message)
            self.mqtt_client.subscribe("robots/+/command_result", handler.handle_message)
            self.mqtt_client.subscribe("robots/+/alert", handler.handle_message)
            
            # Start the client
            self.mqtt_client.start()
            logger.info("MQTT client connected successfully")
            
        except Exception as e:
            logger.error(f"Failed to set up MQTT client: {str(e)}")
            raise

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback for MQTT connection."""
        if rc == 0:
            rprint("[bold green]Connected to MQTT broker[/bold green]")
            # Subscribe to topics
            client.subscribe("robot/+/telemetry")
            client.subscribe("robot/+/status")
        else:
            rprint(f"[bold red]Failed to connect to MQTT broker with code: {rc}[/bold red]")

    def _on_mqtt_message(self, client, userdata, msg):
        """Callback for MQTT messages."""
        try:
            # Process incoming MQTT messages
            topic = msg.topic
            payload = msg.payload.decode()
            rprint(f"[blue]Received MQTT message on topic {topic}: {payload}[/blue]")
            
            # TODO: Process message based on topic and payload
        except Exception as e:
            rprint(f"[bold red]Error processing MQTT message: {str(e)}[/bold red]")

    def publish_command(self, robot_id: str, command: dict):
        """Publish a command to a robot."""
        try:
            if not self.rabbitmq_channel or not self.rabbitmq_channel.is_open:
                raise RuntimeError("RabbitMQ channel is not available")
                
            # Add robot_id to command
            command['robot_id'] = robot_id
            
            # Publish to robot_commands queue
            self.rabbitmq_channel.basic_publish(
                exchange='',
                routing_key='robot_commands',
                body=str(command),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            logger.info(f"Command published for robot {robot_id}: {command}")
            
        except Exception as e:
            logger.error(f"Failed to publish command: {str(e)}")
            raise

    def send_command_to_robot(self, robot_id: str, command: dict) -> bool:
        """Send a command to a robot using RabbitMQ"""
        return self.rabbitmq_client.send_command(robot_id, command)

    def publish_mqtt_message(self, topic: str, message: dict) -> None:
        """Publish a message to an MQTT topic"""
        self.mqtt_client.publish(topic, message)
