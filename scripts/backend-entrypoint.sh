#!/bin/bash
set -e

echo "🚀 Starting Django backend..."

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
./wait-for-it.sh db:5432 --timeout=300 --strict

# Wait for LocalStack
echo "⏳ Waiting for LocalStack..."
./wait-for-it.sh localstack:4566 --timeout=600 --strict

# Run migrations
echo "🔧 Running Django migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Migrate images to S3 and populate database
echo "📁 Migrating images to S3 and populating database..."
python migrate_images_to_s3.py || echo "⚠️ S3 migration failed, continuing with local setup..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start Django development server
echo "✅ Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
