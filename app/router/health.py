"""Health and basic info routes."""

from flask import Blueprint, jsonify

health_router = Blueprint("health", __name__)


@health_router.route("/")
def hello():
    """
    Hello World endpoint
    ---
    responses:
      200:
        description: A simple greeting
    """
    return jsonify({"message": "Hello from Agrobot API!"})


@health_router.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: API health status
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "UP"
    """
    return jsonify({"status": "UP"})
