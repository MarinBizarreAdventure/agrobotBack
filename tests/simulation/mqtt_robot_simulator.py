#!/usr/bin/env python
"""
MQTT Robot Simulator - Simulates robots sending status updates via MQTT
"""
import json
import time
import uuid
import random
import argparse
from datetime import datetime
import paho.mqtt.client as mqtt
from rich.console import Console
from rich.table import Table

console = Console()


class RobotSimulator:
    def __init__(self, robot_id=None, mqtt_host="localhost", mqtt_port=1883):
        self.robot_id = robot_id or str(uuid.uuid4())
        self.client = mqtt.Client(client_id=f"robot-{self.robot_id}")
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.connected = False
        self.x = random.uniform(0, 100)
        self.y = random.uniform(0, 100)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.components = [
            {"id": str(uuid.uuid4()), "name": "Motor", "status": "OK"},
            {"id": str(uuid.uuid4()), "name": "Battery", "status": "OK"},
            {"id": str(uuid.uuid4()), "name": "Camera", "status": "OK"},
            {"id": str(uuid.uuid4()), "name": "Sensor", "status": "OK"},
        ]
        self.actions = []

    def connect(self):
        """Connect to the MQTT broker"""
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            self.client.loop_start()
            self.connected = True
            console.print(
                f"[green]Robot {self.robot_id} connected to MQTT broker[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]Error connecting to MQTT broker: {str(e)}[/red]")
            return False

    def disconnect(self):
        """Disconnect from the MQTT broker"""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            console.print(
                f"[yellow]Robot {self.robot_id} disconnected from MQTT broker[/yellow]"
            )

    def update_position(self):
        """Update robot position with random movement"""
        # Move the robot in a random direction
        self.x += self.direction_x * random.uniform(0.1, 1.0)
        self.y += self.direction_y * random.uniform(0.1, 1.0)

        # Keep the robot within bounds (0-100)
        if self.x < 0 or self.x > 100:
            self.direction_x *= -1  # Reverse direction
            self.x = max(0, min(100, self.x))  # Enforce bounds

        if self.y < 0 or self.y > 100:
            self.direction_y *= -1  # Reverse direction
            self.y = max(0, min(100, self.y))  # Enforce bounds

        return (self.x, self.y)

    def send_location_update(self):
        """Send location update via MQTT"""
        if not self.connected:
            return False

        position = self.update_position()
        payload = {
            "robot_id": self.robot_id,
            "location": [position[0], position[1]],
            "timestamp": datetime.now().isoformat(),
        }

        topic = f"robot/{self.robot_id}/location"
        result = self.client.publish(topic, json.dumps(payload))

        if result.rc == 0:
            console.print(f"[blue]Published location update: {position}[/blue]")
            return True
        else:
            console.print(f"[red]Failed to publish location update[/red]")
            return False

    def send_component_status(self):
        """Send random component status updates"""
        if not self.connected:
            return False

        # Randomly select a component to update
        component = random.choice(self.components)

        # Randomly update status (with higher probability of OK)
        statuses = ["OK", "OK", "OK", "WARNING", "ERROR"]
        component["status"] = random.choice(statuses)

        payload = {
            "robot_id": self.robot_id,
            "component_uuid": component["id"],
            "status": component["status"],
            "details": f"Status update at {datetime.now().isoformat()}",
        }

        topic = f"robot/{self.robot_id}/component/status"
        result = self.client.publish(topic, json.dumps(payload))

        if result.rc == 0:
            console.print(
                f"[blue]Published component status update: {component['name']} is {component['status']}[/blue]"
            )
            return True
        else:
            console.print(f"[red]Failed to publish component status update[/red]")
            return False

    def run_simulation(self, duration=60, interval=2):
        """Run the simulation for a specified duration"""
        if not self.connect():
            console.print("[red]Failed to start simulation[/red]")
            return

        console.print(
            f"[green]Starting simulation for Robot {self.robot_id} for {duration} seconds[/green]"
        )

        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                self.send_location_update()

                # Send component status updates occasionally (1 in 5 chance)
                if random.random() < 0.2:
                    self.send_component_status()

                time.sleep(interval)

        except KeyboardInterrupt:
            console.print("[yellow]Simulation interrupted by user[/yellow]")
        finally:
            self.disconnect()

        console.print(f"[green]Simulation for Robot {self.robot_id} completed[/green]")


def run_multiple_robots(num_robots=3, duration=60, interval=2):
    """Run simulation with multiple robots"""
    console.print(
        f"[bold green]Starting simulation with {num_robots} robots for {duration} seconds[/bold green]"
    )

    table = Table(title="Robot Simulation")
    table.add_column("Robot ID", style="cyan")
    table.add_column("Status", style="green")

    robots = []
    for i in range(num_robots):
        robot_id = f"robot-{i+1}"
        robots.append(RobotSimulator(robot_id=robot_id))
        table.add_row(robot_id, "Initialized")

    console.print(table)

    # Start all robots in separate processes
    import multiprocessing

    processes = []

    for robot in robots:
        p = multiprocessing.Process(
            target=robot.run_simulation, args=(duration, interval)
        )
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    console.print("[bold green]All robot simulations completed[/bold green]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate robots sending MQTT messages"
    )
    parser.add_argument(
        "--robots", type=int, default=3, help="Number of robots to simulate"
    )
    parser.add_argument(
        "--duration", type=int, default=60, help="Duration of simulation in seconds"
    )
    parser.add_argument(
        "--interval", type=float, default=2, help="Interval between updates in seconds"
    )
    parser.add_argument(
        "--host", type=str, default="localhost", help="MQTT broker host"
    )
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")

    args = parser.parse_args()

    run_multiple_robots(
        num_robots=args.robots, duration=args.duration, interval=args.interval
    )
