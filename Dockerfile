# syntax=docker/dockerfile:1

# Use Python 3.12 slim base image
ARG PYTHON_VER=3.12
FROM python:${PYTHON_VER}-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create a non-root user for security
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

WORKDIR /app

# Install required system packages with minimal footprint
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    git \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# (If you use Poetry, copy pyproject.toml and poetry.lock first)
COPY pyproject.toml poetry.lock* requirements.txt* ./

# Install dependencies (choose one: poetry or pip)
# If you use Poetry (recommended for modern projects):
RUN pip install --no-cache-dir --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project files (including src/)
COPY . .

# Set permissions
RUN chown -R appuser:appuser /app && chmod -R 755 /app

USER appuser

# Default command: run the main script from src/
CMD ["python", "src/main.py"]
