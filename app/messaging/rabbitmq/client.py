import json
import threading
import pika
from typing import Callable, Dict, List
from rich import print as rprint


class RabbitMQClient:
    """
    RabbitMQ Client for sending commands to robots and receiving responses.
    Uses pika client in a non-blocking way.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.handlers: Dict[str, List[Callable]] = {}
        self.connected = False
        self._consumer_thread = None
        self._reconnect_delay = 5  # seconds

        # Connection parameters
        self.connection_params = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=pika.PlainCredentials(self.username, self.password),
            heartbeat=600,
            blocked_connection_timeout=300,
        )

    def _connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            self.connected = True
            rprint("[bold green]Connected to RabbitMQ[/bold green]")

            # Declare the needed exchanges and queues
            self.channel.exchange_declare(
                exchange="robot.commands", exchange_type="topic", durable=True
            )

            self.channel.exchange_declare(
                exchange="robot.responses", exchange_type="topic", durable=True
            )

            # Re-subscribe to all queues
            for queue_name in self.handlers.keys():
                self._setup_consumer(queue_name)

            return True
        except Exception as e:
            rprint(f"[bold red]Failed to connect to RabbitMQ: {str(e)}[/bold red]")
            self.connected = False
            return False

    def _setup_consumer(self, queue_name: str):
        """Setup a consumer for a queue"""
        try:
            # Declare queue
            self.channel.queue_declare(queue=queue_name, durable=True)

            # Bind queue to exchange if it's a response queue
            if queue_name.startswith("response."):
                routing_key = queue_name.replace("response.", "")
                self.channel.queue_bind(
                    exchange="robot.responses",
                    queue=queue_name,
                    routing_key=routing_key,
                )

            # Start consuming
            self.channel.basic_consume(
                queue=queue_name, on_message_callback=self._on_message, auto_ack=True
            )

            rprint(f"[green]Set up consumer for queue: {queue_name}[/green]")
            return True
        except Exception as e:
            rprint(
                f"[bold red]Failed to setup consumer for {queue_name}: {str(e)}[/bold red]"
            )
            return False

    def _on_message(self, channel, method, properties, body):
        """Handle incoming messages"""
        queue_name = method.routing_key
        rprint(f"[blue]RabbitMQ message received on {queue_name}[/blue]")

        try:
            payload = json.loads(body.decode())
            if queue_name in self.handlers:
                for handler in self.handlers[queue_name]:
                    handler(payload)
        except json.JSONDecodeError:
            rprint(f"[bold red]Error decoding RabbitMQ message: {body}[/bold red]")
        except Exception as e:
            rprint(f"[bold red]Error processing RabbitMQ message: {str(e)}[/bold red]")

    def start(self):
        """Start the RabbitMQ client in a background thread"""
        if self._consumer_thread is not None and self._consumer_thread.is_alive():
            return

        def run_consumer():
            while True:
                if not self.connected:
                    if not self._connect():
                        rprint(
                            f"[yellow]Reconnecting to RabbitMQ in {self._reconnect_delay} seconds...[/yellow]"
                        )
                        import time

                        time.sleep(self._reconnect_delay)
                        continue

                try:
                    # Start consuming messages
                    rprint("[blue]Starting to consume messages from RabbitMQ[/blue]")
                    self.channel.start_consuming()
                except Exception as e:
                    rprint(f"[bold red]Error in RabbitMQ consumer: {str(e)}[/bold red]")
                    self.connected = False

        self._consumer_thread = threading.Thread(target=run_consumer, daemon=True)
        self._consumer_thread.start()
        rprint("[bold green]RabbitMQ client started in background thread[/bold green]")

    def stop(self):
        """Stop the RabbitMQ client"""
        if self.connected:
            try:
                if self.channel and self.channel.is_open:
                    self.channel.stop_consuming()
                if self.connection and self.connection.is_open:
                    self.connection.close()
            except Exception as e:
                rprint(
                    f"[bold red]Error closing RabbitMQ connection: {str(e)}[/bold red]"
                )

        self.connected = False
        rprint("[bold yellow]RabbitMQ client stopped[/bold yellow]")

    def subscribe(self, queue_name: str, handler: Callable):
        """Subscribe to a queue with a handler function"""
        if queue_name not in self.handlers:
            self.handlers[queue_name] = []
            if self.connected:
                self._setup_consumer(queue_name)

        self.handlers[queue_name].append(handler)
        rprint(f"[green]Subscribed to RabbitMQ queue: {queue_name}[/green]")

    def unsubscribe(self, queue_name: str, handler: Callable = None):
        """Unsubscribe from a queue"""
        if queue_name in self.handlers:
            if handler is None:
                del self.handlers[queue_name]
            else:
                self.handlers[queue_name].remove(handler)
                if not self.handlers[queue_name]:
                    del self.handlers[queue_name]

    def send_command(self, robot_id: str, command: dict):
        """Send a command to a specific robot"""
        if not self.connected:
            rprint(
                "[bold red]Cannot send command: RabbitMQ client not connected[/bold red]"
            )
            return False

        try:
            routing_key = f"robot.{robot_id}"
            payload = json.dumps(command)

            self.channel.basic_publish(
                exchange="robot.commands",
                routing_key=routing_key,
                body=payload,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_type="application/json",
                ),
            )

            rprint(f"[green]Command sent to robot {robot_id}[/green]")
            return True
        except Exception as e:
            rprint(
                f"[bold red]Error sending command to robot {robot_id}: {str(e)}[/bold red]"
            )
            return False
