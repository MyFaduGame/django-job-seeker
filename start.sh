#!/bin/bash
set -e

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations (inside jobSeeker folder)
python3 jobSeeker/manage.py migrate --noinput

# Collect static files
python3 jobSeeker/manage.py collectstatic --noinput

# Start server with Gunicorn
gunicorn jobSeeker.wsgi:application --chdir jobSeeker --bind 0.0.0.0:8000
