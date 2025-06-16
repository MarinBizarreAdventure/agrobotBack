import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from paho.mqtt.client import Client
from app.config import Config

logger = logging.getLogger(__name__)

class MessagingService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.client = Client()
        self._setup_callbacks()
        
    def _setup_callbacks(self):
        """Set up MQTT client callbacks"""
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
    def _on_connect(self, client: Client, userdata: Any, flags: Dict, rc: int):
        """Handle MQTT connection"""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            # Subscribe to topics
            self.client.subscribe("robot/+/heartbeat")
            self.client.subscribe("robot/+/telemetry")
            self.client.subscribe("robot/+/status")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")
            
    def _on_message(self, client: Client, userdata: Any, msg):
        """Handle incoming MQTT messages"""
        try:
            topic = msg.topic
            payload = msg.payload.decode()
            logger.debug(f"Received message on topic {topic}: {payload}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            
    def _on_disconnect(self, client: Client, userdata: Any, rc: int):
        """Handle MQTT disconnection"""
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker with code: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")
            
    def start(self):
        """Start the messaging service"""
        try:
            # Set username and password
            self.client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
            
            # Connect to broker
            self.client.connect(Config.MQTT_BROKER, Config.MQTT_PORT)
            
            # Start network loop
            self.client.loop_start()
            logger.info("Messaging service started")
            
        except Exception as e:
            logger.error(f"Failed to start messaging service: {str(e)}")
            raise
            
    def stop(self):
        """Stop the messaging service"""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Messaging service stopped")
        except Exception as e:
            logger.error(f"Error stopping messaging service: {str(e)}")
            
    def publish(self, topic: str, payload: str, qos: int = 0):
        """Publish a message to a topic"""
        try:
            result = self.client.publish(topic, payload, qos=qos)
            if result.rc != 0:
                logger.error(f"Failed to publish message to {topic}: {result.rc}")
            else:
                logger.debug(f"Published message to {topic}: {payload}")
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
