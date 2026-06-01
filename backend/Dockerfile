FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies for some Python packages (psycopg2, bcrypt, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Ensure gunicorn and psycopg2 are available
RUN pip install --no-cache-dir gunicorn psycopg2-binary

# Copy application source
COPY . /app

# Copy and make entrypoint script executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV FLASK_APP=run.py

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
