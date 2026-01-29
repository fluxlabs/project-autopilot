# Autopilot Dashboard Backend Dockerfile
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy orchestrator code
COPY ../../../*.py /app/orchestrator/
COPY ../../../config.yaml /app/orchestrator/

# Copy backend code
COPY . .

# Add orchestrator to Python path
ENV PYTHONPATH="/app/orchestrator:${PYTHONPATH}"

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
