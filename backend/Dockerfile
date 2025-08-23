# backend/Dockerfile
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (optional but helpful for builds/requests SSL etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install deps first for better layer caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY backend/. .

# Expose backend port
EXPOSE 8000

# Use gunicorn/uvicorn worker to serve FastAPI
# If your main is main.py and app is 'app' object
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
