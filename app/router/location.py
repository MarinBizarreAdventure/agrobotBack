"""Robot location routes."""

from flask import Blueprint, jsonify, request
from app.data.database import SessionLocal
from app.api.robot.service import RobotService
from app.api.step.model import RobotStep
from app.api.step.service import StepService

location_router = Blueprint("location", __name__)


@location_router.route("/robots/<robot_id>/location", methods=["GET"])
def get_robot_location(robot_id: str):
    """
    Get the latest location of a robot
    ---
    tags:
      - Locations
    parameters:
      - name: robot_id
        in: path
        schema:
          type: string
        required: true
        description: UUID of the robot
    responses:
      200:
        description: Latest location
        content:
          application/json:
            schema:
              type: object
              properties:
                robot_id:
                  type: string
                location:
                  type: array
                  items:
                    type: number
      404:
        description: No location data available or robot not found
    """
    db = SessionLocal()
    try:
        robot_service = RobotService(db)

        # Check if robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404

        location = robot_service.get_latest_location(robot_id)
        if not location:
            return jsonify({"error": "No location data available"}), 404

        return jsonify({"robot_id": robot_id, "location": location})
    finally:
        db.close()


@location_router.route("/robots/<robot_id>/location", methods=["POST"])
def update_robot_location(robot_id: str):
    """
    Post new location for a robot
    ---
    tags:
      - Locations
    parameters:
      - name: robot_id
        in: path
        schema:
          type: string
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              location:
                type: array
                items:
                  type: number
    responses:
      200:
        description: Location updated
      400:
        description: Invalid input
    """
    location_data = request.json
    if not location_data or "location" not in location_data:
        return jsonify({"error": "No location data provided"}), 400

    try:
        location = location_data["location"]
        if not isinstance(location, list) or len(location) != 2:
            return jsonify({"error": "Location must be an array of [x, y]"}), 400

        x, y = location

        db = SessionLocal()
        try:
            # First check if the robot exists
            robot_service = RobotService(db)
            robot = robot_service.get_robot(robot_id)
            if not robot:
                return jsonify({"error": "Robot not found"}), 404

            # Create a new step for the robot
            step_service = StepService(db)
            step = RobotStep(location=(float(x), float(y)))
            step_service.create_step(step, robot_id)

            return jsonify(
                {
                    "message": "Location updated",
                    "robot_id": robot_id,
                    "location": [x, y],
                }
            )
        finally:
            db.close()
    except Exception as e:
        return jsonify({"error": f"Error updating location: {str(e)}"}), 400
