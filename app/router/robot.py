"""Robot management routes."""

from flask import Blueprint, jsonify, request
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

robot_router = Blueprint("robot", __name__)


@robot_router.route("/robots", methods=["GET"])
def list_robots():
    """
    List all robots
    ---
    tags:
      - Robots
    responses:
      200:
        description: List of robots
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Robot'
    """
    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        robots = robot_service.list_robots()
        return jsonify([robot.dict() for robot in robots])
    finally:
        db.close()


@robot_router.route("/robots/<robot_id>", methods=["GET"])
def get_robot(robot_id: str):
    """
    Get robot by ID
    ---
    tags:
      - Robots
    parameters:
      - name: robot_id
        in: path
        schema:
          type: string
        required: true
        description: UUID of the robot
    responses:
      200:
        description: Robot details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Robot'
      404:
        description: Robot not found
    """
    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404
        return jsonify(robot.dict())
    finally:
        db.close()


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


@robot_router.route("/api/v1/backend/register", methods=["POST"])
def register_robot():
    """
    Register a new robot with the Agrobot system
    ---
    tags:
      - Robot Registration
    summary: Register a new robot
    description: |
      Register a new robot with the Agrobot system. This endpoint is used by robots to establish their connection with the backend.
      
      Example request:
      ```json
      {
        "robot_id": "agrobot-rpi-001",
        "robot_name": "AgroBot Raspberry Pi",
        "version": "1.0.0",
        "robot_ip_address": "192.168.1.100",
        "robot_port": 8000,
        "capabilities": [
          {
            "name": "GPS",
            "supported": true,
            "details": {}
          }
        ],
        "location": {
          "latitude": 47.1234,
          "longitude": 28.5678,
          "altitude": 100.0,
          "timestamp": "2024-03-20T12:00:00Z"
        },
        "software_version": "1.0.0",
        "metadata": {}
      }
      ```
    operationId: registerRobot
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - robot_id
              - robot_name
              - version
              - robot_ip_address
              - robot_port
              - capabilities
              - software_version
            properties:
              robot_id:
                type: string
                description: Unique ID of the robot
                example: "agrobot-rpi-001"
              robot_name:
                type: string
                description: Name of the robot
                example: "AgroBot Raspberry Pi"
              version:
                type: string
                description: Current software version
                example: "1.0.0"
              robot_ip_address:
                type: string
                description: Robot's current IP address
                example: "192.168.1.100"
              robot_port:
                type: integer
                description: Robot's port
                example: 8000
              capabilities:
                type: array
                description: List of robot capabilities
                items:
                  type: object
                  properties:
                    name:
                      type: string
                      example: "GPS"
                    supported:
                      type: boolean
                      example: true
                    details:
                      type: object
                      example: {}
              location:
                type: object
                description: Current location if GPS fix is available
                properties:
                  latitude:
                    type: number
                    example: 47.1234
                  longitude:
                    type: number
                    example: 28.5678
                  altitude:
                    type: number
                    example: 100.0
                  timestamp:
                    type: string
                    format: date-time
                    example: "2024-03-20T12:00:00Z"
              software_version:
                type: string
                description: Current software version
                example: "1.0.0"
              metadata:
                type: object
                description: Additional metadata
                example: {}
    responses:
      200:
        description: Registration successful
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Robot registered successfully"
                robot_id:
                  type: string
                  example: "agrobot-rpi-001"
                robot_config:
                  type: object
                  properties:
                    heartbeat_interval:
                      type: integer
                      example: 30
                    telemetry_interval:
                      type: integer
                      example: 60
                    mqtt_topics:
                      type: object
                      properties:
                        heartbeat:
                          type: string
                          example: "robots/agrobot-rpi-001/heartbeat"
                        telemetry:
                          type: string
                          example: "robots/agrobot-rpi-001/telemetry"
                        command_result:
                          type: string
                          example: "robots/agrobot-rpi-001/command_result"
                        alert:
                          type: string
                          example: "robots/agrobot-rpi-001/alert"
      400:
        description: Invalid request data
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Invalid request data"
                robot_id:
                  type: string
                  nullable: true
                robot_config:
                  type: object
                  nullable: true
      500:
        description: Server error
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Internal server error"
                robot_id:
                  type: string
                  nullable: true
                robot_config:
                  type: object
                  nullable: true
    """
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "message": "Request must be JSON",
                "robot_id": None,
                "robot_config": None
            }), 400

        register_data = RegisterRequest(**request.json)
        db = SessionLocal()
        try:
            robot_service = RobotService(db)
            response = robot_service.register_robot(register_data)
            return jsonify(response.dict())
        finally:
            db.close()
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error registering robot: {str(e)}",
            "robot_id": request.json.get("robot_id") if request.is_json else None,
            "robot_config": None
        }), 400


@robot_router.route("/api/v1/robot/heartbeat", methods=["POST"])
def robot_heartbeat():
    """
    Receive robot heartbeat
    ---
    tags:
      - Robot Health
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/HeartbeatRequest'
    responses:
      200:
        description: Heartbeat response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HeartbeatResponse'
    """
    try:
        heartbeat_data = HeartbeatRequest(**request.json)
        db = SessionLocal()
        try:
            robot_service = RobotService(db)
            response = robot_service.process_heartbeat(heartbeat_data)
            return jsonify(response.dict())
        finally:
            db.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@robot_router.route("/api/v1/robot/telemetry", methods=["POST"])
def robot_telemetry():
    """
    Receive robot telemetry data
    ---
    tags:
      - Robot Telemetry
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/TelemetryBatchRequest'
    responses:
      200:
        description: Telemetry response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TelemetryBatchResponse'
    """
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
        return jsonify({"error": str(e)}), 400


@robot_router.route("/api/v1/robot/command_result", methods=["POST"])
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
        return jsonify({"error": str(e)}), 400


@robot_router.route("/api/v1/robot/alert", methods=["POST"])
def robot_alert():
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
        return jsonify({"error": str(e)}), 400


@robot_router.route("/api/v1/robot/commands", methods=["GET"])
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
    """
    robot_id = request.args.get("robot_id")
    if not robot_id:
        return jsonify({"error": "robot_id is required"}), 400

    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        response = robot_service.get_pending_commands(robot_id)
        return jsonify(response.dict())
    finally:
        db.close()
