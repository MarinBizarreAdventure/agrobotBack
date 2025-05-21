"""Robot management routes."""

from flask import Blueprint, jsonify, request
from app.data.database import SessionLocal
from app.api.robot.service import RobotService
from app.api.robot.model import Robot as ApiRobot

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
