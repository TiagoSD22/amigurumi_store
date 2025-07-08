"""
Setup script for the Django backend
"""
import os
import sys
import django
from pathlib import Path

# Add the current directory to the Python path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amigurumi_store.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def setup_database():
    """Run Django migrations and setup"""
    print("Setting up Django database...")
    
    # Create migrations
    print("Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'products'])
        print("✓ Migrations created")
    except Exception as e:
        print(f"Migration creation: {e}")
    
    # Apply migrations
    print("Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Migrations applied")
    except Exception as e:
        print(f"Migration application: {e}")
    
    # Check if tables exist
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✓ Database tables created: {[table[0] for table in tables]}")

if __name__ == '__main__':
    setup_database()
    print("Django setup complete!")
