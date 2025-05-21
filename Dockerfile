FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata
COPY pyproject.toml poetry.lock* /app/

# Install poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

# Copy the rest of the code
COPY . /app

# Environment
ENV FLASK_APP=app.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV DOCKER_ENV=true
ENV PYTHONPATH=/app

EXPOSE 5000

# Start the API
ENTRYPOINT ["poetry", "run", "agrobot"]
