from functools import wraps
from flask import request, jsonify
from app.data.robot.repository import RobotRepository
from app.data.database import SessionLocal
from http import HTTPStatus

def verify_robot_ip(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        robot_ip = request.json.get('robot_ip') if request.is_json else None
        
        if not robot_ip:
            return jsonify({
                "error": "Robot IP is required",
                "message": "Please provide a valid robot IP"
            }), HTTPStatus.BAD_REQUEST

        with SessionLocal() as session:
            repo = RobotRepository(session)
            robot = repo.get_by_ip(robot_ip)
            
            if not robot:
                return jsonify({
                    "error": "Robot not found",
                    "message": f"No robot found with IP: {robot_ip}"
                }), HTTPStatus.NOT_FOUND
            
            # Update robot's IP address if it has changed
            if robot.ip_address != client_ip:
                repo.update(robot.robot_id, {"ip_address": client_ip})
                robot.ip_address = client_ip

        return f(*args, **kwargs)
    return decorated_function 