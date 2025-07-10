#!/bin/bash
set -e

echo "🎯 Amigurumi Store - Docker Setup"
echo "================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans || true

# Build and start all services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."

echo "Waiting for database..."
timeout 60 bash -c 'until docker-compose exec -T db pg_isready -U postgres; do sleep 2; done'

echo "Waiting for LocalStack..."
timeout 120 bash -c 'until curl -s http://localhost:4566/health > /dev/null; do sleep 2; done'

echo "Waiting for backend..."
timeout 120 bash -c 'until curl -s http://localhost:8000/api/products/ > /dev/null; do sleep 2; done'

echo "Waiting for frontend..."
timeout 60 bash -c 'until curl -s http://localhost:3000 > /dev/null; do sleep 2; done'

echo ""
echo "🎉 Amigurumi Store is now running!"
echo "=================================="
echo ""
echo "📱 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000/api/products/"
echo "👤 Django Admin: http://localhost:8000/admin/ (admin/admin123)"
echo "🗄️  Database:    localhost:5432 (postgres/postgres)"
echo "☁️  LocalStack:  http://localhost:4566"
echo ""
echo "📋 Available commands:"
echo "  docker-compose logs -f [service]  # View logs"
echo "  docker-compose stop              # Stop services"
echo "  docker-compose down              # Stop and remove containers"
echo "  docker-compose restart [service] # Restart a service"
echo ""
echo "🔍 Service status:"
docker-compose ps
