import json
import threading
import paho.mqtt.client as mqtt
from typing import Callable, Dict, List
from rich import print as rprint


class MQTTClient:
    """
    MQTT Client for receiving real-time data from robots.
    Uses paho-mqtt client in a non-blocking way.
    """

    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.handlers: Dict[str, List[Callable]] = {}
        self.connected = False
        self._thread = None

    def _on_connect(self, client, userdata, flags, rc):
        rprint(f"[bold green]MQTT Connected with result code {rc}[/bold green]")
        self.connected = rc == 0
        # Re-subscribe to topics on reconnect
        for topic in self.handlers.keys():
            client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        rprint(f"[blue]MQTT message received on {msg.topic}[/blue]")
        try:
            payload = json.loads(msg.payload.decode())
            if msg.topic in self.handlers:
                for handler in self.handlers[msg.topic]:
                    handler(payload)
        except json.JSONDecodeError:
            rprint(f"[bold red]Error decoding MQTT message: {msg.payload}[/bold red]")
        except Exception as e:
            rprint(f"[bold red]Error processing MQTT message: {str(e)}[/bold red]")

    def start(self):
        """Start the MQTT client in a background thread"""
        if self._thread is not None and self._thread.is_alive():
            return

        def run_client():
            try:
                self.client.connect(self.broker_host, self.broker_port, 60)
                self.client.loop_forever()
            except Exception as e:
                rprint(f"[bold red]MQTT connection error: {str(e)}[/bold red]")
                self.connected = False

        self._thread = threading.Thread(target=run_client, daemon=True)
        self._thread.start()
        rprint("[bold green]MQTT client started in background thread[/bold green]")

    def stop(self):
        """Stop the MQTT client"""
        if self.connected:
            self.client.disconnect()
        self.connected = False
        rprint("[bold yellow]MQTT client stopped[/bold yellow]")

    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to a topic with a handler function"""
        if topic not in self.handlers:
            self.handlers[topic] = []
            if self.connected:
                self.client.subscribe(topic)
        
        self.handlers[topic].append(handler)
        rprint(f"[green]Subscribed to MQTT topic: {topic}[/green]")

    def unsubscribe(self, topic: str, handler: Callable = None):
        """Unsubscribe from a topic"""
        if topic in self.handlers:
            if handler is None:
                del self.handlers[topic]
                self.client.unsubscribe(topic)
            else:
                self.handlers[topic].remove(handler)
                if not self.handlers[topic]:
                    del self.handlers[topic]
                    self.client.unsubscribe(topic)
                    
    def publish(self, topic: str, message: dict):
        """Publish a message to a topic"""
        if self.connected:
            payload = json.dumps(message)
            self.client.publish(topic, payload)
            rprint(f"[green]Published message to {topic}[/green]")
        else:
            rprint("[bold red]Cannot publish: MQTT client not connected[/bold red]")
