#!/usr/bin/env python
"""
Command Sender - Sends commands to robots via RabbitMQ for testing
"""
import json
import uuid
import argparse
import random
from datetime import datetime
import pika
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()


class CommandSender:
    def __init__(
        self,
        rabbitmq_host="localhost",
        rabbitmq_port=5672,
        rabbitmq_user="agrobot",
        rabbitmq_pass="agrobot",
    ):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pass = rabbitmq_pass
        self.connection = None
        self.channel = None
        self.connected = False
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

            # Declare exchange
            self.channel.exchange_declare(
                exchange=self.command_exchange, exchange_type="topic", durable=True
            )

            self.connected = True
            console.print("[green]Connected to RabbitMQ[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Error connecting to RabbitMQ: {str(e)}[/red]")
            return False

    def disconnect(self):
        """Disconnect from RabbitMQ"""
        if self.connected and self.connection and self.connection.is_open:
            self.connection.close()
            console.print("[yellow]Disconnected from RabbitMQ[/yellow]")
            self.connected = False

    def send_command(self, robot_id, command_type, parameters=None):
        """Send a command to a specific robot"""
        if not self.connected:
            console.print("[red]Cannot send command: Not connected[/red]")
            return False

        command_id = str(uuid.uuid4())
        command = {
            "command_id": command_id,
            "command_type": command_type,
            "parameters": parameters or {},
            "timestamp": datetime.now().isoformat(),
        }

        routing_key = f"robot.{robot_id}"

        try:
            self.channel.basic_publish(
                exchange=self.command_exchange,
                routing_key=routing_key,
                body=json.dumps(command),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type="application/json",
                ),
            )
            console.print(
                f"[green]Sent command {command_id} of type {command_type} to robot {robot_id}[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]Error sending command: {str(e)}[/red]")
            return False

    def interactive_mode(self):
        """Run interactive command sender mode"""
        if not self.connect():
            console.print("[red]Failed to connect to RabbitMQ[/red]")
            return

        try:
            while True:
                console.print(
                    "\n[bold blue]Command Sender - Interactive Mode[/bold blue]"
                )

                robot_id = Prompt.ask(
                    "[yellow]Enter robot ID[/yellow]", default="robot-1"
                )

                command_types = [
                    "MOVE_TO",
                    "TAKE_PICTURE",
                    "COLLECT_SAMPLE",
                    "START_MONITORING",
                    "STOP_MONITORING",
                    "RETURN_HOME",
                    "POWER_OFF",
                ]

                console.print("[yellow]Available command types:[/yellow]")
                for i, cmd_type in enumerate(command_types):
                    console.print(f"  {i+1}. {cmd_type}")

                selection = Prompt.ask(
                    "[yellow]Select command type (number or name)[/yellow]", default="1"
                )

                try:
                    # Try to interpret as number
                    idx = int(selection) - 1
                    if 0 <= idx < len(command_types):
                        command_type = command_types[idx]
                    else:
                        command_type = selection
                except ValueError:
                    # Not a number, use as is
                    command_type = selection

                # Build parameters based on command type
                parameters = {}

                if command_type == "MOVE_TO":
                    parameters["x"] = float(
                        Prompt.ask(
                            "[yellow]Enter X coordinate[/yellow]", default="50.0"
                        )
                    )
                    parameters["y"] = float(
                        Prompt.ask(
                            "[yellow]Enter Y coordinate[/yellow]", default="50.0"
                        )
                    )
                    parameters["speed"] = float(
                        Prompt.ask("[yellow]Enter speed[/yellow]", default="1.0")
                    )

                elif command_type == "TAKE_PICTURE":
                    parameters["resolution"] = Prompt.ask(
                        "[yellow]Enter resolution[/yellow]", default="1080p"
                    )
                    parameters["format"] = Prompt.ask(
                        "[yellow]Enter format[/yellow]", default="jpg"
                    )

                elif command_type == "COLLECT_SAMPLE":
                    parameters["sample_type"] = Prompt.ask(
                        "[yellow]Enter sample type[/yellow]", default="soil"
                    )
                    parameters["amount"] = float(
                        Prompt.ask("[yellow]Enter amount[/yellow]", default="10.0")
                    )

                # Send the command
                self.send_command(robot_id, command_type, parameters)

                # Ask to continue
                if not Confirm.ask(
                    "[yellow]Send another command?[/yellow]", default=True
                ):
                    break

        except KeyboardInterrupt:
            console.print("[yellow]Interactive mode interrupted by user[/yellow]")
        finally:
            self.disconnect()

    def batch_mode(self, num_commands=5, robot_ids=None):
        """Send a batch of random commands to robots"""
        if not self.connect():
            console.print("[red]Failed to connect to RabbitMQ[/red]")
            return

        if robot_ids is None:
            robot_ids = [f"robot-{i+1}" for i in range(3)]

        command_types = [
            "MOVE_TO",
            "TAKE_PICTURE",
            "COLLECT_SAMPLE",
            "START_MONITORING",
            "STOP_MONITORING",
            "RETURN_HOME",
        ]

        try:
            console.print(f"[blue]Sending {num_commands} random commands...[/blue]")

            for i in range(num_commands):
                robot_id = random.choice(robot_ids)
                command_type = random.choice(command_types)

                # Generate random parameters based on command type
                parameters = {}

                if command_type == "MOVE_TO":
                    parameters = {
                        "x": random.uniform(0, 100),
                        "y": random.uniform(0, 100),
                        "speed": random.uniform(0.5, 2.0),
                    }

                elif command_type == "TAKE_PICTURE":
                    parameters = {
                        "resolution": random.choice(["720p", "1080p", "4K"]),
                        "format": random.choice(["jpg", "png", "raw"]),
                    }

                elif command_type == "COLLECT_SAMPLE":
                    parameters = {
                        "sample_type": random.choice(["soil", "water", "air", "plant"]),
                        "amount": random.uniform(5, 50),
                    }

                self.send_command(robot_id, command_type, parameters)

            console.print("[green]Batch command sending completed[/green]")

        except Exception as e:
            console.print(f"[red]Error in batch mode: {str(e)}[/red]")
        finally:
            self.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send commands to robots via RabbitMQ")
    parser.add_argument("--batch", action="store_true", help="Run in batch mode")
    parser.add_argument(
        "--commands",
        type=int,
        default=5,
        help="Number of commands to send in batch mode",
    )
    parser.add_argument("--host", type=str, default="localhost", help="RabbitMQ host")
    parser.add_argument("--port", type=int, default=5672, help="RabbitMQ port")
    parser.add_argument("--user", type=str, default="agrobot", help="RabbitMQ username")
    parser.add_argument(
        "--password", type=str, default="agrobot", help="RabbitMQ password"
    )

    args = parser.parse_args()

    sender = CommandSender(
        rabbitmq_host=args.host,
        rabbitmq_port=args.port,
        rabbitmq_user=args.user,
        rabbitmq_pass=args.password,
    )

    if args.batch:
        sender.batch_mode(num_commands=args.commands)
    else:
        sender.interactive_mode()
