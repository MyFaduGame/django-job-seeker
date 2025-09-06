#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Django Project Setup..."

cd jobSeeker

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
  echo "🐍 Python3 not found. Installing..."
  sudo apt update
  sudo apt install -y python3 python3-pip python3-venv
else
  echo "✅ Python3 already installed."
fi

# Ensure pip is installed
if ! command -v pip3 &>/dev/null; then
  echo "📦 pip3 not found. Installing..."
  sudo apt install -y python3-pip
else
  echo "✅ pip3 already installed."
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
  echo "🔹 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "🔹 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
  echo "📦 Installing dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "⚠️ requirements.txt not found, skipping dependency installation."
fi

# Apply migrations
echo "🗄️ Applying migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files
echo "📂 Collecting static files..."
python3 manage.py collectstatic --noinput

# Start the server
echo "🌍 Starting Django development server at http://127.0.0.1:8000/"
python3 manage.py runserver 0.0.0.0:8000
