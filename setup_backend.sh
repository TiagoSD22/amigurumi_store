#!/bin/bash

# Amigurumi Store Backend Setup Script

echo "Setting up Amigurumi Store Backend..."

# Navigate to backend directory
cd backend

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment (Windows)
echo "Activating virtual environment..."
# For Windows
source venv/Scripts/activate
# For Linux/Mac (uncomment the line below)
# source venv/bin/activate

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
echo "You can skip this step by pressing Ctrl+C"
python manage.py createsuperuser

# Populate database with sample data
echo "Populating database with sample data..."
python populate_db.py

echo "Backend setup complete!"
echo "To start the server, run: python manage.py runserver"
