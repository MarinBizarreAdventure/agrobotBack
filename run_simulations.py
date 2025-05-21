#!/usr/bin/env python
"""
Convenience script to run robot simulations
"""
import argparse
import subprocess
import sys
from rich.console import Console

console = Console()


def run_simulation(simulation_type, **kwargs):
    """Run a specific simulation"""
    if simulation_type == "mqtt":
        from tests.simulation.mqtt_robot_simulator import run_multiple_robots

        run_multiple_robots(
            num_robots=kwargs.get("robots", 3),
            duration=kwargs.get("duration", 60),
            interval=kwargs.get("interval", 2),
        )
    elif simulation_type == "rabbitmq":
        from tests.simulation.rabbitmq_robot_responder import run_multiple_responders

        run_multiple_responders(
            num_robots=kwargs.get("robots", 3), duration=kwargs.get("duration", 600)
        )
    elif simulation_type == "combined":
        from tests.simulation.combined_simulator import main

        sys.argv = [sys.argv[0]]  # Reset args for the imported main
        if "robots" in kwargs:
            sys.argv.extend(["--robots", str(kwargs["robots"])])
        if "duration" in kwargs:
            sys.argv.extend(["--duration", str(kwargs["duration"])])
        if "interval" in kwargs:
            sys.argv.extend(["--interval", str(kwargs["interval"])])
        main()
    elif simulation_type == "db_test":
        from tests.integration.db_rabbitmq_test import DatabaseIntegrationTest

        test = DatabaseIntegrationTest()
        test.run_test(
            num_robots=kwargs.get("robots", 2),
            num_commands=kwargs.get("commands", 3),
            num_locations=kwargs.get("locations", 5),
        )
    else:
        console.print(f"[red]Unknown simulation type: {simulation_type}[/red]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run robot simulations")
    parser.add_argument(
        "type",
        choices=["mqtt", "rabbitmq", "combined", "db_test"],
        help="Type of simulation to run",
    )
    parser.add_argument(
        "--robots", type=int, default=3, help="Number of robots to simulate"
    )
    parser.add_argument(
        "--duration", type=int, default=60, help="Duration of simulation in seconds"
    )
    parser.add_argument(
        "--interval", type=float, default=2, help="Interval between messages (for MQTT)"
    )
    parser.add_argument(
        "--commands",
        type=int,
        default=3,
        help="Number of commands per robot (for db_test)",
    )
    parser.add_argument(
        "--locations",
        type=int,
        default=5,
        help="Number of location updates per robot (for db_test)",
    )

    args = parser.parse_args()

    # Run the selected simulation
    run_simulation(
        args.type,
        robots=args.robots,
        duration=args.duration,
        interval=args.interval,
        commands=args.commands,
        locations=args.locations,
    )
