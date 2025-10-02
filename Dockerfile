FROM python:3.11-slim

# Recommended Python flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory and ensure it's on PYTHONPATH
WORKDIR /app
ENV PYTHONPATH=/app

# System deps (curl useful for health checks/debug)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the source
COPY . /app

# Cloud Run listens on PORT (injected), default 8080
ENV PORT=8080

# Expose for local parity (harmless in Cloud Run)
EXPOSE 8080

# Robust launcher: finds your FastAPI app automatically
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
