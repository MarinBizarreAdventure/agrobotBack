"""Robot component routes."""

from flask import Blueprint, jsonify, request
from app.data.database import SessionLocal
from app.api.robot.service import RobotService
from app.api.component.service import ComponentService
from app.data.component.model import ComponentDiagnosisState

component_router = Blueprint("component", __name__)


@component_router.route(
    "/robots/<robot_id>/components/<component_uuid>", methods=["PATCH"]
)
def update_component_status(robot_id: str, component_uuid: str):
    """
    Update a component's status
    ---
    parameters:
      - name: robot_id
        in: path
        type: string
        required: true
        description: ID of the robot
      - name: component_uuid
        in: path
        type: string
        required: true
        description: UUID of the component
      - name: status
        in: body
        required: true
        schema:
          type: object
          properties:
            current_status:
              type: string
              description: New status for the component (OK, WARNING, ERROR, UNKNOWN)
    responses:
      200:
        description: Component status updated successfully
      404:
        description: Robot or component not found
      400:
        description: Invalid status data
    """
    status_data = request.json
    if not status_data or "current_status" not in status_data:
        return jsonify({"error": "No status data provided"}), 400

    try:
        new_status = status_data["current_status"]
        # Validate the status value
        try:
            ComponentDiagnosisState(new_status)
        except ValueError:
            return jsonify({"error": f"Invalid status value: {new_status}"}), 400

        db = SessionLocal()
        try:
            # First check if the robot exists
            robot_service = RobotService(db)
            robot = robot_service.get_robot(robot_id)
            if not robot:
                return jsonify({"error": "Robot not found"}), 404

            # Get the component service
            component_service = ComponentService(db)

            # Get the component
            component = component_service.get_component(component_uuid)
            if not component:
                return jsonify({"error": "Component not found"}), 404

            # Update component status
            component.current_status = new_status
            updated_component = component_service.update_component(component)

            return jsonify(
                {
                    "message": "Component status updated",
                    "component_uuid": component_uuid,
                    "current_status": updated_component.current_status,
                }
            )
        finally:
            db.close()
    except Exception as e:
        return jsonify({"error": f"Error updating component status: {str(e)}"}), 400


@component_router.route("/robots/<robot_id>/components", methods=["GET"])
def list_components(robot_id):
    """
    List components for a robot
    ---
    tags:
      - Components
    parameters:
      - name: robot_id
        in: path
        schema:
          type: string
        required: true
    responses:
      200:
        description: List of components
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Component'
    """
    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        component_service = ComponentService(db)

        # Check if the robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404

        # Get components for the robot
        components = component_service.get_components_by_robot_id(robot_id)

        return jsonify(components), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching components: {str(e)}"}), 400
    finally:
        db.close()


@component_router.route("/robots/<robot_id>/components", methods=["POST"])
def create_component(robot_id):
    """
    Create a component for a robot
    ---
    tags:
      - Components
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
            $ref: '#/components/schemas/Component'
    responses:
      201:
        description: Component created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Component'
    """
    component_data = request.json
    if not component_data:
        return jsonify({"error": "No component data provided"}), 400

    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        component_service = ComponentService(db)

        # Check if the robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404

        # Create the component
        new_component = component_service.create_component(robot_id, component_data)

        return jsonify(new_component), 201
    except Exception as e:
        return jsonify({"error": f"Error creating component: {str(e)}"}), 400
    finally:
        db.close()


@component_router.route(
    "/robots/<robot_id>/components/<component_uuid>", methods=["GET"]
)
def get_component(robot_id: str, component_uuid: str):
    """
    Get a component's details
    ---
    parameters:
      - name: robot_id
        in: path
        type: string
        required: true
        description: ID of the robot
      - name: component_uuid
        in: path
        type: string
        required: true
        description: UUID of the component
    responses:
      200:
        description: Component details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Component'
      404:
        description: Robot or component not found
    """
    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        component_service = ComponentService(db)

        # Check if the robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404

        # Get the component
        component = component_service.get_component(component_uuid)
        if not component:
            return jsonify({"error": "Component not found"}), 404

        return jsonify(component), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching component details: {str(e)}"}), 400
    finally:
        db.close()


@component_router.route(
    "/robots/<robot_id>/components/<component_uuid>", methods=["DELETE"]
)
def delete_component(robot_id: str, component_uuid: str):
    """
    Delete a component
    ---
    parameters:
      - name: robot_id
        in: path
        type: string
        required: true
        description: ID of the robot
      - name: component_uuid
        in: path
        type: string
        required: true
        description: UUID of the component
    responses:
      204:
        description: Component deleted successfully
      404:
        description: Robot or component not found
    """
    db = SessionLocal()
    try:
        robot_service = RobotService(db)
        component_service = ComponentService(db)

        # Check if the robot exists
        robot = robot_service.get_robot(robot_id)
        if not robot:
            return jsonify({"error": "Robot not found"}), 404

        # Delete the component
        component_service.delete_component(component_uuid)

        return jsonify({"message": "Component deleted"}), 204
    except Exception as e:
        return jsonify({"error": f"Error deleting component: {str(e)}"}), 400
    finally:
        db.close()
