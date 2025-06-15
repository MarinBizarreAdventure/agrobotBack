import os
from dotenv import load_dotenv
from rich import print as rprint

# Load environment variables
DOCKER_ENV = os.environ.get("DOCKER_ENV", "false")
if DOCKER_ENV == "true":
    load_dotenv(".env.docker")
    rprint("[bold blue]Running in Docker environment[/bold blue]")
else:
    load_dotenv()
    rprint("[bold blue]Running in local environment[/bold blue]")

class Config:
    # Environment
    DOCKER_ENV = DOCKER_ENV

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agrobot:agrobot@localhost:5432/agrobot")

    # MQTT Configuration
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", "agrobot")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "agrobot")

    # RabbitMQ Configuration
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "agrobot")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "agrobot")
    RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "agrobot")

    # Application Configuration
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    PORT = int(os.getenv("PORT", "5000"))
    HOST = os.getenv("HOST", "0.0.0.0")

    @classmethod
    def get_mqtt_config(cls):
        return {
            "broker": cls.MQTT_BROKER,
            "port": cls.MQTT_PORT,
            "username": cls.MQTT_USERNAME,
            "password": cls.MQTT_PASSWORD
        }

    @classmethod
    def get_rabbitmq_config(cls):
        return {
            "host": cls.RABBITMQ_HOST,
            "port": cls.RABBITMQ_PORT,
            "username": cls.RABBITMQ_USER,
            "password": cls.RABBITMQ_PASSWORD,
            "virtual_host": cls.RABBITMQ_VHOST
        } 