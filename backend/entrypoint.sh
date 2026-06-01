#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting Gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:5000 run:app
