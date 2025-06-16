from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class HeartbeatRequest(BaseModel):
    robot_id: str = Field(..., description="ID of the robot sending heartbeat")
    status: str = Field(..., description="Current status of the robot")
    battery_level: float = Field(..., description="Current battery level (0-100)")
    location: Dict[str, float] = Field(..., description="Current location coordinates")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional robot metadata")

    class Config:
        schema_extra = {
            "example": {
                "robot_id": "robot_123",
                "status": "online",
                "battery_level": 85.5,
                "location": {
                    "x": 10.5,
                    "y": 20.3,
                    "z": 0.0
                },
                "metadata": {
                    "temperature": 25.5,
                    "humidity": 60.0
                }
            }
        }

class HeartbeatResponse(BaseModel):
    success: bool = Field(..., description="Whether the heartbeat was processed successfully")
    pending_commands: List[Dict[str, Any]] = Field(default_factory=list, description="List of pending commands")
    robot_config: Optional[Dict[str, Any]] = Field(None, description="Updated robot configuration if any")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "pending_commands": [
                    {
                        "command_id": "cmd_123",
                        "command_type": "move",
                        "parameters": {
                            "x": 15.0,
                            "y": 25.0,
                            "z": 0.0
                        }
                    }
                ],
                "robot_config": {
                    "update_interval": 5,
                    "max_speed": 2.0
                }
            }
        }

class TelemetryData(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the telemetry data")
    sensor_id: str = Field(..., description="ID of the sensor")
    value: float = Field(..., description="Sensor value")
    unit: str = Field(..., description="Unit of measurement")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional sensor metadata")

    class Config:
        schema_extra = {
            "example": {
                "timestamp": "2024-03-20T10:00:00Z",
                "sensor_id": "temp_1",
                "value": 25.5,
                "unit": "celsius",
                "metadata": {
                    "location": "main_chamber",
                    "accuracy": 0.1
                }
            }
        }

class TelemetryBatchRequest(BaseModel):
    robot_id: str = Field(..., description="ID of the robot sending telemetry")
    timestamp: datetime = Field(..., description="Batch timestamp")
    data: List[TelemetryData] = Field(..., description="List of telemetry data points")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional batch metadata")

    class Config:
        schema_extra = {
            "example": {
                "robot_id": "robot_123",
                "timestamp": "2024-03-20T10:00:00Z",
                "data": [
                    {
                        "timestamp": "2024-03-20T10:00:00Z",
                        "sensor_id": "temp_1",
                        "value": 25.5,
                        "unit": "celsius",
                        "metadata": {
                            "location": "main_chamber"
                        }
                    }
                ],
                "metadata": {
                    "batch_id": "batch_123",
                    "version": "1.0"
                }
            }
        }

class TelemetryBatchResponse(BaseModel):
    success: bool = Field(..., description="Whether the telemetry batch was processed successfully")
    processed_count: int = Field(..., description="Number of telemetry data points processed")
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="List of any processing errors")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "processed_count": 1,
                "errors": []
            }
        }

class Robot(BaseModel):
    robot_id: str = Field(..., description="Unique identifier for the robot")
    name: str = Field(..., description="Name of the robot")
    status: str = Field(..., description="Current status of the robot")
    capabilities: Dict[str, Any] = Field(..., description="Robot capabilities")
    location: Dict[str, float] = Field(..., description="Current location coordinates")
    battery_level: float = Field(..., description="Current battery level (0-100)")
    last_heartbeat: datetime = Field(..., description="Timestamp of last heartbeat")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional robot metadata")

    class Config:
        schema_extra = {
            "example": {
                "robot_id": "robot_123",
                "name": "AgroBot-1",
                "status": "online",
                "capabilities": {
                    "movement": {
                        "max_speed": 2.0,
                        "max_payload": 50.0
                    },
                    "sensors": ["temperature", "humidity", "gps"]
                },
                "location": {
                    "x": 10.5,
                    "y": 20.3,
                    "z": 0.0
                },
                "battery_level": 85.5,
                "last_heartbeat": "2024-03-20T10:00:00Z",
                "metadata": {
                    "model": "AgroBot-X1",
                    "firmware_version": "1.2.3"
                }
            }
        } 