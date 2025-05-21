# Agrobot

Backend for the Agrobot project - a robotics platform for agricultural automation.

## Project Structure

```
app/
  - api/        # API models (Pydantic)
  - data/       # Database models (SQLAlchemy)
  - messaging/  # MQTT and RabbitMQ clients and handlers
    - mqtt/     # MQTT specific code
    - rabbitmq/ # RabbitMQ specific code
  - app.py      # Main application entry point
```

## Getting Started

1. Start the infrastructure services:

```bash
docker-compose up -d
```

2. Run the application:

```bash
poetry install
poetry run agrobot
```

## Running the Server

After you have started the infrastructure and installed dependencies:

```
# Start database, MQTT and RabbitMQ
docker-compose up -d

# Install Python deps and run locally
poetry install
poetry run agrobot
```

Or build and run the API in Docker:

```
docker-compose up --build web
```

## Accessing the API

- Base URL: http://localhost:5000  
- Health check: GET  /health  
- List robots:   GET  /robots  
- Swagger UI:    http://localhost:5000/apidocs  (interactive API documentation)

You can now send commands, view robot data, and explore endpoints via the Swagger UI.

## Messaging Infrastructure

Agrobot uses two messaging protocols for robot communication:

- **MQTT**: For lightweight, real-time status updates (location, component status, action updates)
- **RabbitMQ**: For reliable command delivery and responses

### MQTT Topics

- `robot/{robot_id}/location` - Location updates from robots
- `robot/{robot_id}/component/status` - Component status updates
- `robot/{robot_id}/action/update` - Action status updates

### RabbitMQ Queues

- Exchange: `robot.commands` - For sending commands to robots
- Exchange: `robot.responses` - For receiving command responses
- Queue: `response.commands` - Queue for command responses
- Queue: `telemetry.data` - Queue for robot telemetry data

## Development

This project uses:
- Poetry for dependency management
- SQLAlchemy for database ORM
- Flask for the web API
- PostgreSQL for data storage
- MQTT for real-time messaging
- RabbitMQ for reliable command delivery
