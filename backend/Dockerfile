FROM python:3.12-slim

# No .pyc files in the image; logs go straight to stdout (Cloud Logging reads stdout).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Dependencies first: this layer is cached until requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Don't run as root inside the container.
RUN useradd --create-home --uid 1000 app
USER app

# Cloud Run tells the container which port to listen on via $PORT (8080 there).
# Shell form so ${PORT} is expanded; exec so uvicorn gets SIGTERM directly.
# --proxy-headers: trust X-Forwarded-* from Cloud Run's front end (correct https URLs).
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips="*"
