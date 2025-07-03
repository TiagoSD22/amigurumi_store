@echo off
REM Amigurumi Store Backend Setup Script for Windows

echo Setting up Amigurumi Store Backend...

REM Navigate to backend directory
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser (optional)
echo Creating superuser...
echo You can skip this step by pressing Ctrl+C
python manage.py createsuperuser

REM Populate database with sample data
echo Populating database with sample data...
python populate_db.py

echo Backend setup complete!
echo To start the server, run: python manage.py runserver
pause
