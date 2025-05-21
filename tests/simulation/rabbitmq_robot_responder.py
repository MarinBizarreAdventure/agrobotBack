#!/usr/bin/env python
"""
RabbitMQ Robot Responder - Simulates robots responding to commands via RabbitMQ
"""
import json
import time
import uuid
import random
import argparse
import sys
import os
from datetime import datetime
import pika
from rich.console import Console

# Add the project root to the Python path if needed
if __name__ == "__main__":
    # Get the absolute path of the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    # Add to Python path if not already there
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

console = Console()


class RobotResponder:
    def __init__(
        self,
        robot_id=None,
        rabbitmq_host="localhost",
        rabbitmq_port=5672,
        rabbitmq_user="agrobot",
        rabbitmq_pass="agrobot",
    ):
        self.robot_id = robot_id or str(uuid.uuid4())
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pass = rabbitmq_pass
        self.connection = None
        self.channel = None
        self.connected = False
        self.queue_name = f"robot.{self.robot_id}"
        self.response_exchange = "robot.responses"
        self.command_exchange = "robot.commands"

    def connect(self):
        """Connect to RabbitMQ"""
        try:
            # Set up connection parameters
            credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
            parameters = pika.ConnectionParameters(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                credentials=credentials,
                heartbeat=60,
            )

            # Establish connection
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            # Declare exchanges
            self.channel.exchange_declare(
                exchange=self.command_exchange, exchange_type="topic", durable=True
            )

            self.channel.exchange_declare(
                exchange=self.response_exchange, exchange_type="topic", durable=True
            )

            # Declare queue for this robot's commands
            result = self.channel.queue_declare(
                queue="", exclusive=True  # Let RabbitMQ generate a queue name
            )
            queue_name = result.method.queue

            # Bind queue to exchange with routing key for this robot
            self.channel.queue_bind(
                exchange=self.command_exchange,
                queue=queue_name,
                routing_key=self.queue_name,
            )

            # Set up consumer
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=self.on_command_received,
                auto_ack=True,
            )

            self.connected = True
            console.print(f"[green]Robot {self.robot_id} connected to RabbitMQ[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Error connecting to RabbitMQ: {str(e)}[/red]")
            return False

    def disconnect(self):
        """Disconnect from RabbitMQ"""
        if self.connected and self.connection and self.connection.is_open:
            self.connection.close()
            console.print(
                f"[yellow]Robot {self.robot_id} disconnected from RabbitMQ[/yellow]"
            )
            self.connected = False

    def on_command_received(self, channel, method, properties, body):
        """Handle received commands"""
        try:
            command = json.loads(body)
            command_id = command.get("command_id", "unknown")
            command_type = command.get("command_type", "unknown")
            parameters = command.get("parameters", {})

            console.print(
                f"[blue]Robot {self.robot_id} received command {command_id} of type {command_type}[/blue]"
            )
            console.print(f"[blue]Parameters: {parameters}[/blue]")

            # Simulate processing time
            processing_time = random.uniform(0.5, 2.0)
            console.print(
                f"[blue]Processing command for {processing_time:.2f} seconds...[/blue]"
            )
            time.sleep(processing_time)

            # Determine success or failure (90% success rate)
            success = random.random() < 0.9
            status = "SUCCESS" if success else "FAILURE"
            message = (
                "Command executed successfully"
                if success
                else "Command execution failed"
            )

            # Send response
            response = {
                "robot_id": self.robot_id,
                "command_id": command_id,
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "data": {"execution_time_ms": int(processing_time * 1000)},
            }

            self.send_response(response)

            # Also send telemetry data after command execution
            self.send_telemetry()

        except Exception as e:
            console.print(f"[red]Error processing command: {str(e)}[/red]")

    def send_response(self, response):
        """Send command response"""
        if not self.connected:
            console.print("[red]Cannot send response: Not connected[/red]")
            return False

        try:
            routing_key = "response.commands"
            self.channel.basic_publish(
                exchange=self.response_exchange,
                routing_key=routing_key,
                body=json.dumps(response),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type="application/json",
                ),
            )
            console.print(
                f"[green]Sent response for command {response['command_id']}: {response['status']}[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]Error sending command response: {str(e)}[/red]")
            return False

    def send_telemetry(self):
        """Send telemetry data"""
        if not self.connected:
            return False

        try:
            # Generate random telemetry data
            telemetry = {
                "robot_id": self.robot_id,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "battery": random.uniform(20, 100),
                    "cpu_usage": random.uniform(10, 90),
                    "memory_usage": random.uniform(20, 80),
                    "temperature": random.uniform(25, 45),
                    "disk_space": random.uniform(10, 95),
                },
            }

            routing_key = "telemetry.data"
            self.channel.basic_publish(
                exchange=self.response_exchange,
                routing_key=routing_key,
                body=json.dumps(telemetry),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type="application/json",
                ),
            )
            console.print(f"[blue]Sent telemetry data[/blue]")
            return True
        except Exception as e:
            console.print(f"[red]Error sending telemetry data: {str(e)}[/red]")
            return False

    def run(self, duration=600):
        """Run the robot responder for a specified duration"""
        if not self.connect():
            console.print("[red]Failed to start robot responder[/red]")
            return

        console.print(
            f"[green]Robot {self.robot_id} is now listening for commands for {duration} seconds[/green]"
        )

        try:
            start_time = time.time()
            # Run until duration is reached or interrupted
            while time.time() - start_time < duration:
                # Process messages for 1 second at a time to check duration
                self.connection.process_data_events(time_limit=1)

                # Occasionally send telemetry even without commands
                if random.random() < 0.05:  # 5% chance each second
                    self.send_telemetry()
        except KeyboardInterrupt:
            console.print("[yellow]Robot responder interrupted by user[/yellow]")
        finally:
            self.disconnect()

        console.print(f"[green]Robot {self.robot_id} responder completed[/green]")


def run_multiple_responders(num_robots=3, duration=600):
    """Run multiple robot responders"""
    console.print(
        f"[bold green]Starting {num_robots} robot responders for {duration} seconds[/bold green]"
    )

    # Start all robots in separate processes
    import multiprocessing

    processes = []

    for i in range(num_robots):
        robot_id = f"robot-{i+1}"
        responder = RobotResponder(robot_id=robot_id)

        p = multiprocessing.Process(target=responder.run, args=(duration,))
        processes.append(p)
        p.start()
        console.print(f"[green]Started responder for Robot {robot_id}[/green]")

    # Wait for all processes to finish
    for p in processes:
        p.join()

    console.print("[bold green]All robot responders completed[/bold green]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate robots responding to RabbitMQ commands"
    )
    parser.add_argument(
        "--robots", type=int, default=3, help="Number of robots to simulate"
    )
    parser.add_argument(
        "--duration", type=int, default=600, help="Duration to listen in seconds"
    )
    parser.add_argument("--host", type=str, default="localhost", help="RabbitMQ host")
    parser.add_argument("--port", type=int, default=5672, help="RabbitMQ port")
    parser.add_argument("--user", type=str, default="agrobot", help="RabbitMQ username")
    parser.add_argument(
        "--password", type=str, default="agrobot", help="RabbitMQ password"
    )

    args = parser.parse_args()

    run_multiple_responders(num_robots=args.robots, duration=args.duration)
