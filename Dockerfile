# syntax=docker/dockerfile:1

# Set Python version as build argument
ARG PYTHON_VER=3.12

# Use slim Python base image
FROM python:${PYTHON_VER}-slim-bullseye

# Set environment variables for Python and application path
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1

# Create a non-root user and group for the application
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Set the working directory
WORKDIR /app

# Install required system libraries for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependency files to the image
COPY pyproject.toml poetry.lock* requirements.txt* ./

# Install Python dependencies with Poetry
RUN pip install --no-cache-dir --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the application source code
COPY . .

# Set permissions for the application directory
RUN chown -R appuser:appuser /app && chmod -R 755 /app

# Switch to the non-root user
USER appuser

# Set the default command to run the entrypoint script
CMD ["python", "src/main.py"]
