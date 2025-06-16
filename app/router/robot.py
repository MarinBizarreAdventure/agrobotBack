"""Robot management routes."""

from flask import Blueprint, jsonify, request, current_app
from http import HTTPStatus
from flasgger import swag_from
from app.data.database import SessionLocal
from app.api.robot.service import RobotService
from app.api.robot.dto import (
    Robot as ApiRobot,
    RegisterRequest,
    RegisterResponse,
    HeartbeatRequest,
    HeartbeatResponse,
    TelemetryBatchRequest,
    TelemetryBatchResponse,
    CommandResultRequest,
    CommandResultResponse,
    AlertRequest,
    AlertResponse,
    PollCommandsResponse
)
from app.data.robot.repository import RobotRepository
from app.api.robot.schemas import Robot
from app.middleware.ip_verification import verify_robot_ip

robot_router = Blueprint("robot", __name__, url_prefix="/api/v1")


def get_robot_service():
    session = SessionLocal()
    try:
        return RobotService(session)
    finally:
        session.close()


@robot_router.route("/heartbeat", methods=["POST"])
@verify_robot_ip
@swag_from({
    'tags': ['robot'],
    'summary': 'Process robot heartbeat',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': HeartbeatRequest.schema()
        }
    ],
    'responses': {
        200: {
            'description': 'Heartbeat processed successfully',
            'schema': HeartbeatResponse.schema()
        },
        400: {
            'description': 'Invalid request data',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def process_heartbeat():
    """Process a robot heartbeat."""
    try:
        robot_service = get_robot_service()
        heartbeat_data = HeartbeatRequest(**request.json)
        response = robot_service.process_heartbeat(heartbeat_data)
        return jsonify(response.dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        current_app.logger.error(f"Error processing heartbeat: {str(e)}")
        return jsonify({"error": f"Error processing heartbeat: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR


@robot_router.route("/telemetry", methods=["POST"])
@verify_robot_ip
@swag_from({
    'tags': ['robot'],
    'summary': 'Process robot telemetry data',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': TelemetryBatchRequest.schema()
        }
    ],
    'responses': {
        200: {
            'description': 'Telemetry data processed successfully',
            'schema': TelemetryBatchResponse.schema()
        },
        400: {
            'description': 'Invalid request data',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def process_telemetry():
    """Process robot telemetry data."""
    try:
        telemetry_data = TelemetryBatchRequest(**request.json)
        db = SessionLocal()
        try:
            robot_service = RobotService(db)
            response = robot_service.process_telemetry(telemetry_data)
            return jsonify(response.dict())
        finally:
            db.close()
    except Exception as e:
        current_app.logger.error(f"Error processing telemetry: {str(e)}")
        return jsonify({"error": f"Error processing telemetry: {str(e)}"}), HTTPStatus.BAD_REQUEST


@robot_router.route("/", methods=["GET"])
@swag_from({
    'tags': ['robot'],
    'summary': 'Get all robots',
    'responses': {
        200: {
            'description': 'List of robots',
            'schema': {
                'type': 'array',
                'items': Robot.schema()
            }
        }
    }
})
def list_robots():
    """Get all robots."""
    robot_service = get_robot_service()
    robots = robot_service.list_robots()
    return jsonify([robot.dict() for robot in robots])


@robot_router.route("/<robot_id>", methods=["GET"])
@swag_from({
    'tags': ['robot'],
    'summary': 'Get robot by ID',
    'parameters': [
        {
            'name': 'robot_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the robot to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Robot found',
            'schema': Robot.schema()
        },
        404: {
            'description': 'Robot not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_robot(robot_id: str):
    """Get a robot by ID."""
    robot_service = get_robot_service()
    robot = robot_service.get_robot(robot_id)
    if not robot:
      return jsonify({"error": f"Robot {robot_id} not found"}), HTTPStatus.NOT_FOUND
    return jsonify(robot.dict())


@robot_router.route("/robots", methods=["POST"])
def create_robot():
    """
    Create a new robot
    ---
    tags:
      - Robots
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Robot'
    responses:
      201:
        description: Robot created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Robot'
      400:
        description: Invalid input
    """
    robot_data = request.json
    if not robot_data:
        return jsonify({"error": "No robot data provided"}), 400

    try:
        # Convert request data to API model
        api_robot = ApiRobot(**robot_data)

        db = SessionLocal()
        try:
            robot_service = RobotService(db)
            created_robot = robot_service.create_robot(api_robot)
            return jsonify(created_robot.dict()), 201
        finally:
            db.close()
    except Exception as e:
        return jsonify({"error": f"Error creating robot: {str(e)}"}), 400


@robot_router.route("/backend/register", methods=["POST"])
def register_robot():
    """Register a new robot with the Agrobot system"""
    try:
        register_data = RegisterRequest(**request.json)
        
        with SessionLocal() as db:
            service = RobotService(db)
            response = service.register_robot(register_data)
            return jsonify(response.dict()), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error registering robot: {str(e)}")
        return jsonify({
            "error": f"Error registering robot: {str(e)}",
            "message": "Failed to register robot"
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@robot_router.route("/command_result", methods=["POST"])
@verify_robot_ip
def command_result():
    """
    Receive command execution result
    ---
    tags:
      - Robot Commands
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CommandResultRequest'
    responses:
      200:
        description: Command result response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommandResultResponse'
    """
    try:
        result_data = CommandResultRequest(**request.json)
        db = SessionLocal()
        try:
            robot_service = RobotService(db)
            response = robot_service.process_command_result(result_data)
            return jsonify(response.dict())
        finally:
            db.close()
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@robot_router.route("/alert", methods=["POST"])
@verify_robot_ip
def process_alert():
    """
    Receive robot alert
    ---
    tags:
      - Robot Alerts
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/AlertRequest'
    responses:
      200:
        description: Alert response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AlertResponse'
    """
    try:
        alert_data = AlertRequest(**request.json)
        db = SessionLocal()
        try:
            robot_service = RobotService(db)
            response = robot_service.process_alert(alert_data)
            return jsonify(response.dict())
        finally:
            db.close()
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@robot_router.route("/api/v1/backend/commands/pending", methods=["GET"])
def poll_commands():
    """
    Poll for pending commands
    ---
    tags:
      - Robot Commands
    parameters:
      - name: robot_id
        in: query
        schema:
          type: string
        required: true
        description: ID of the robot
    responses:
      200:
        description: Pending commands
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PollCommandsResponse'
      400:
        description: Missing robot_id
      404:
        description: Robot not found
    """
    robot_id = request.args.get("robot_id")
    if not robot_id:
        return jsonify({"error": "robot_id is required"}), 400

    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        
        # Check if robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404
            
        response = robot_service.get_pending_commands(robot_id)
        return jsonify(response.dict())
    except Exception as e:
        return jsonify({"error": f"Error polling commands: {str(e)}"}), 500
    finally:
        db.close()
