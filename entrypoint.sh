#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Starting application..."
exec "$@"