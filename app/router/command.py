"""Robot command routes."""

from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime
from app.data.database import SessionLocal

command_router = Blueprint("command", __name__)

# Reference to the global messaging service, will be set by app.py
messaging_service = None


def set_messaging_service(service):
    """Set the messaging service for command handling"""
    global messaging_service
    messaging_service = service


@command_router.route("/robots/<robot_id>/command", methods=["POST"])
def send_robot_command(robot_id: str):
    """
    Send command to a robot
    ---
    tags:
      - Commands
    parameters:
      - name: robot_id
        in: path
        schema:
          type: string
        required: true
        description: UUID of the robot
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              command_type:
                type: string
              parameters:
                type: object
    responses:
      200:
        description: Command sent
      400:
        description: Invalid input
      404:
        description: Robot not found
      500:
        description: Failed to send command
    """
    from app.api.robot.service import RobotService

    command_data = request.json
    if not command_data:
        return jsonify({"error": "No command data provided"}), 400

    if messaging_service is None:
        return jsonify({"error": "Messaging service not initialized"}), 500

    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        robot_service.set_messaging_service(messaging_service)

        # Check if robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404

        # Send command
        command = {
            "command_id": command_data.get("command_id", str(uuid.uuid4())),
            "command_type": command_data.get("command_type"),
            "parameters": command_data.get("parameters", {}),
            "timestamp": datetime.now().isoformat(),
        }

        if robot_service.send_command_to_robot(robot_id, command):
            return jsonify(
                {
                    "message": "Command sent successfully",
                    "command_id": command["command_id"],
                }
            )
        else:
            return jsonify({"error": "Failed to send command"}), 500
    finally:
        db.close()
