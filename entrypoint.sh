#!/bin/bash
set -e

echo "Running migrations..."
python app/manage.py migrate

echo "Starting server..."
exec python app/manage.py runserver 0.0.0.0:8000