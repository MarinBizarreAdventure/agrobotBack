# Agrobot API Endpoints Documentation

## Base URL
All endpoints are prefixed with `/api/v1`

## Authentication
Currently, the API does not require authentication for robot communication endpoints.

## Endpoints

### Robot Registration and Management

#### Register Robot
```http
POST /api/v1/backend/register
```
Register a new robot or update an existing one.

**Request Body:**
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

**Response:**
```json
{
  "success": true,
  "message": "Robot registered successfully",
  "robot_id": "agrobot-rpi-001",
  "robot_config": {
    "heartbeat_interval": 30,
    "telemetry_interval": 60,
    "mqtt_topics": {
      "heartbeat": "robots/agrobot-rpi-001/heartbeat",
      "telemetry": "robots/agrobot-rpi-001/telemetry",
      "command_result": "robots/agrobot-rpi-001/command_result",
      "alert": "robots/agrobot-rpi-001/alert"
    }
  }
}
```

#### List All Robots
```http
GET /robots
```
Get a list of all registered robots.

**Response:**
```json
[
  {
    "robot_id": "agrobot-rpi-001",
    "name": "AgroBot Raspberry Pi",
    "ip_address": "192.168.1.100",
    "port": 8000,
    "version": "1.0.0",
    "software_version": "1.0.0",
    "capabilities": [...],
    "status": "online",
    "last_seen": "2024-03-20T12:00:00Z",
    "health_metrics": {},
    "current_location": {},
    "robot_metadata": {}
  }
]
```

#### Get Robot Details
```http
GET /robots/{robot_id}
```
Get details for a specific robot.

**Response:**
```json
{
  "robot_id": "agrobot-rpi-001",
  "name": "AgroBot Raspberry Pi",
  "ip_address": "192.168.1.100",
  "port": 8000,
  "version": "1.0.0",
  "software_version": "1.0.0",
  "capabilities": [...],
  "status": "online",
  "last_seen": "2024-03-20T12:00:00Z",
  "health_metrics": {},
  "current_location": {},
  "robot_metadata": {}
}
```

### Robot Health and Status

#### Send Heartbeat
```http
GET/POST /api/v1/robot/heartbeat
```
Send a heartbeat to indicate robot is alive.

**Query Parameters (GET):**
- `robot_id`: Robot identifier

**Request Body (POST):**
```json
{
  "robot_id": "agrobot-rpi-001",
  "timestamp": "2024-03-20T12:00:00Z",
  "status": "online",
  "health_metrics": {
    "cpu_usage": 45.2,
    "memory_usage": 60.5,
    "battery_level": 85.0
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Heartbeat received",
  "timestamp": "2024-03-20T12:00:00Z"
}
```

#### Send Telemetry Data
```http
POST /api/v1/robot/telemetry
```
Send robot telemetry data.

**Request Body:**
```json
{
  "robot_id": "agrobot-rpi-001",
  "timestamp": "2024-03-20T12:00:00Z",
  "data": {
    "location": {
      "latitude": 47.1234,
      "longitude": 28.5678,
      "altitude": 100.0
    },
    "sensors": {
      "temperature": 25.5,
      "humidity": 60.0,
      "pressure": 1013.2
    },
    "system": {
      "cpu_usage": 45.2,
      "memory_usage": 60.5,
      "battery_level": 85.0
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Telemetry data received",
  "timestamp": "2024-03-20T12:00:00Z"
}
```

#### Send Alert
```http
POST /api/v1/robot/alert
```
Send a robot alert.

**Request Body:**
```json
{
  "robot_id": "agrobot-rpi-001",
  "timestamp": "2024-03-20T12:00:00Z",
  "alert_type": "warning",
  "message": "Low battery level",
  "details": {
    "battery_level": 15.0,
    "estimated_time_remaining": "30 minutes"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Alert received",
  "timestamp": "2024-03-20T12:00:00Z"
}
```

### Robot Commands

#### Poll for Pending Commands
```http
GET /api/v1/backend/commands/pending
```
Get pending commands for a robot.

**Query Parameters:**
- `robot_id`: Robot identifier

**Response:**
```json
{
  "robot_id": "agrobot-rpi-001",
  "commands": [
    {
      "command_id": "cmd-123",
      "command_type": "move",
      "parameters": {
        "x": 100,
        "y": 200,
        "speed": 50
      },
      "timestamp": "2024-03-20T12:00:00Z"
    }
  ]
}
```

#### Send Command Result
```http
POST /api/v1/robot/command_result
```
Send the result of a command execution.

**Request Body:**
```json
{
  "robot_id": "agrobot-rpi-001",
  "command_id": "cmd-123",
  "status": "completed",
  "result": {
    "success": true,
    "message": "Command executed successfully",
    "data": {
      "final_position": {
        "x": 100,
        "y": 200
      }
    }
  },
  "error": null,
  "timestamp": "2024-03-20T12:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Command result received",
  "timestamp": "2024-03-20T12:00:00Z"
}
```

### Component Management

#### List Robot Components
```http
GET /robots/{robot_id}/components
```
Get all components for a robot.

**Response:**
```json
[
  {
    "component_id": "comp-123",
    "robot_id": "agrobot-rpi-001",
    "name": "GPS Module",
    "type": "sensor",
    "status": "operational",
    "diagnosis_state": "ok",
    "last_maintenance": "2024-03-01T00:00:00Z",
    "metadata": {}
  }
]
```

#### Create Component
```http
POST /robots/{robot_id}/components
```
Create a new component for a robot.

**Request Body:**
```json
{
  "name": "GPS Module",
  "type": "sensor",
  "status": "operational",
  "diagnosis_state": "ok",
  "metadata": {}
}
```

**Response:**
```json
{
  "component_id": "comp-123",
  "robot_id": "agrobot-rpi-001",
  "name": "GPS Module",
  "type": "sensor",
  "status": "operational",
  "diagnosis_state": "ok",
  "last_maintenance": "2024-03-20T12:00:00Z",
  "metadata": {}
}
```

#### Get Component Details
```http
GET /robots/{robot_id}/components/{component_uuid}
```
Get details for a specific component.

**Response:**
```json
{
  "component_id": "comp-123",
  "robot_id": "agrobot-rpi-001",
  "name": "GPS Module",
  "type": "sensor",
  "status": "operational",
  "diagnosis_state": "ok",
  "last_maintenance": "2024-03-01T00:00:00Z",
  "metadata": {}
}
```

#### Update Component Status
```http
PATCH /robots/{robot_id}/components/{component_uuid}
```
Update a component's status.

**Request Body:**
```json
{
  "current_status": "warning",
  "diagnosis_state": "needs_maintenance",
  "metadata": {
    "last_error": "Signal strength low",
    "error_count": 5
  }
}
```

**Response:**
```json
{
  "component_id": "comp-123",
  "robot_id": "agrobot-rpi-001",
  "name": "GPS Module",
  "type": "sensor",
  "status": "warning",
  "diagnosis_state": "needs_maintenance",
  "last_maintenance": "2024-03-01T00:00:00Z",
  "metadata": {
    "last_error": "Signal strength low",
    "error_count": 5
  }
}
```

#### Delete Component
```http
DELETE /robots/{robot_id}/components/{component_uuid}
```
Delete a component.

**Response:**
```json
{
  "message": "Component deleted"
}
```

### Location Management

#### Get Robot Location
```http
GET /robots/{robot_id}/location
```
Get the latest location of a robot.

**Response:**
```json
{
  "robot_id": "agrobot-rpi-001",
  "location": [47.1234, 28.5678]
}
```

#### Update Robot Location
```http
POST /robots/{robot_id}/location
```
Update a robot's location.

**Request Body:**
```json
{
  "location": [47.1234, 28.5678]
}
```

**Response:**
```json
{
  "message": "Location updated",
  "robot_id": "agrobot-rpi-001",
  "location": [47.1234, 28.5678]
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid request data"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Status Codes

- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Notes

1. All timestamps are in ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
2. All coordinates are in decimal degrees
3. All measurements are in metric units
4. All endpoints return JSON responses
5. All endpoints accept JSON request bodies where applicable 