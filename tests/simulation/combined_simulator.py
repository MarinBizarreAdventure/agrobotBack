#!/usr/bin/env python
"""
Combined Robot Simulator - Runs both MQTT and RabbitMQ simulators together
"""
import argparse
import multiprocessing
from rich.console import Console

# Import the simulator modules
from mqtt_robot_simulator import run_multiple_robots
from rabbitmq_robot_responder import run_multiple_responders

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Run combined robot simulators")
    parser.add_argument(
        "--robots", type=int, default=3, help="Number of robots to simulate"
    )
    parser.add_argument("--duration", type=int, default=600, help="Duration in seconds")
    parser.add_argument(
        "--interval", type=float, default=2, help="MQTT update interval in seconds"
    )

    args = parser.parse_args()

    console.print("[bold green]Starting combined robot simulator[/bold green]")
    console.print(
        f"[blue]Simulating {args.robots} robots for {args.duration} seconds[/blue]"
    )

    # Start MQTT simulator in a separate process
    mqtt_process = multiprocessing.Process(
        target=run_multiple_robots, args=(args.robots, args.duration, args.interval)
    )

    # Start RabbitMQ responder in a separate process
    rabbitmq_process = multiprocessing.Process(
        target=run_multiple_responders, args=(args.robots, args.duration)
    )

    # Start both processes
    mqtt_process.start()
    rabbitmq_process.start()

    # Wait for both to finish
    mqtt_process.join()
    rabbitmq_process.join()

    console.print("[bold green]Combined simulation completed[/bold green]")


if __name__ == "__main__":
    main()
