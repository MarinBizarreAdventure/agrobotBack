"""Robot command routes."""

from flask import Blueprint, jsonify, request, current_app
import uuid
from datetime import datetime
from app.data.database import SessionLocal
from typing import List, Optional
from http import HTTPStatus
from flasgger import swag_from

from app.api.command.service import CommandService
from app.data.command.repository import CommandRepository
from app.data.command.dto import (
    CommandCreateDTO,
    CommandUpdateDTO,
    CommandStatusUpdateDTO
)
from app.data.enums import CommandStatus, CommandType

command_router = Blueprint("command", __name__, url_prefix="/api/commands")

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

def get_command_service():
    db = SessionLocal()
    try:
        return CommandService(CommandRepository(db))
    finally:
        db.close()

@command_router.route("/<command_id>", methods=["GET"])
def get_command(command_id: str):
    """Get a command by ID"""
    try:
        with SessionLocal() as db:
            service = CommandService(db)
            command = service.get_command(command_id)
            if not command:
                return jsonify({"error": "Command not found"}), HTTPStatus.NOT_FOUND
            return jsonify(command.dict()), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error getting command: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@command_router.route("/robot/<robot_id>/pending", methods=["GET"])
def get_pending_commands(robot_id: str):
    """Get pending commands for a robot"""
    try:
        with SessionLocal() as db:
            service = CommandService(db)
            commands = service.get_pending_commands(robot_id)
            return jsonify([cmd.dict() for cmd in commands]), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error getting pending commands: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@command_router.route("/", methods=["POST"])
def create_command():
    """Create a new command"""
    try:
        data = request.get_json()
        command_data = CommandCreateDTO(**data)
        
        with SessionLocal() as db:
            service = CommandService(db)
            command = service.create_command(command_data)
            return jsonify(command.dict()), HTTPStatus.CREATED
    except Exception as e:
        current_app.logger.error(f"Error creating command: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@command_router.route("/<command_id>", methods=["PUT"])
def update_command(command_id: str):
    """Update a command"""
    try:
        data = request.get_json()
        command_data = CommandUpdateDTO(**data)
        
        with SessionLocal() as db:
            service = CommandService(db)
            command = service.update_command(command_id, command_data)
            if not command:
                return jsonify({"error": "Command not found"}), HTTPStatus.NOT_FOUND
            return jsonify(command.dict()), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error updating command: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@command_router.route("/<command_id>/status", methods=["PUT"])
def update_command_status(command_id: str):
    """Update command status"""
    try:
        data = request.get_json()
        status_data = CommandStatusUpdateDTO(**data)
        
        with SessionLocal() as db:
            service = CommandService(db)
            command = service.update_command_status(command_id, status_data)
            if not command:
                return jsonify({"error": "Command not found"}), HTTPStatus.NOT_FOUND
            return jsonify(command.dict()), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error updating command status: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@command_router.route("/<command_id>", methods=["DELETE"])
def delete_command(command_id: str):
    """Delete a command"""
    try:
        with SessionLocal() as db:
            service = CommandService(db)
            if service.delete_command(command_id):
                return "", HTTPStatus.NO_CONTENT
            return jsonify({"error": "Command not found"}), HTTPStatus.NOT_FOUND
    except Exception as e:
        current_app.logger.error(f"Error deleting command: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
