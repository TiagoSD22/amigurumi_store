#!/bin/bash

echo "🧹 Removing Windows-specific files..."

# Remove Windows batch and PowerShell files
rm -f *.bat *.ps1

# Remove Windows-specific Python scripts
rm -f complete_setup.py
rm -f full_setup_no_docker.py
rm -f populate_database_only.py
rm -f setup_localstack.py
rm -f setup_with_terraform.py
rm -f start_localstack_host.py
rm -f start_localstack_simple.py
rm -f test_django_api.py
rm -f test_localstack.py

# Remove Windows-specific documentation
rm -f FIXED_SETUP.md
rm -f LOCALSTACK_SETUP.md

# Remove old populate scripts
rm -f populate_database.py

# Remove LocalStack data directory
rm -rf .localstack/

# Remove package-lock.json if it exists (will be regenerated in Docker)
rm -f frontend/package-lock.json

echo "✅ Windows-specific files removed!"
echo "📋 Remaining files are Docker-compatible."
