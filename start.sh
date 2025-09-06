#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Django Project..."

cd jobSeeker

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  echo "🔹 Activating virtual environment..."
  source venv/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
  echo "📦 Installing dependencies..."
  pip install -r requirements.txt
fi

# Apply migrations
echo "🗄️ Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "🌍 Starting Django development server at http://127.0.0.1:8000/"
python manage.py runserver 0.0.0.0:8000
