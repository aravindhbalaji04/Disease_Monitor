#!/bin/bash
# Start script for Render deployment
# This ensures the Flask app starts correctly with gunicorn

echo "Starting Disease Monitoring Portal..."
echo "Python version: $(python --version)"
echo "Gunicorn version: $(gunicorn --version)"

# Start the application
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
