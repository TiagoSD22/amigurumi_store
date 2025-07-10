#!/bin/bash
set -e

echo "🎯 Amigurumi Store - Docker Setup (Fixed LocalStack)"
echo "=================================================="

# Function to cleanup LocalStack containers and volumes
cleanup_localstack() {
    echo "🧹 Cleaning up existing LocalStack containers..."
    docker stop amigurumi_localstack 2>/dev/null || true
    docker rm amigurumi_localstack 2>/dev/null || true
    docker stop amigurumi_terraform 2>/dev/null || true
    docker rm amigurumi_terraform 2>/dev/null || true
    
    # Clean up volumes if they're causing issues
    echo "🗑️ Removing LocalStack volume if it exists..."
    docker volume rm amigurumi_store_localstack_data 2>/dev/null || true
    
    echo "✅ LocalStack cleanup completed"
}

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Ask user which compose file to use
echo "Choose LocalStack setup:"
echo "1. Alternative setup (recommended - uses official LocalStack image)"
echo "2. Original setup (custom LocalStack build)"
read -p "Enter choice [1-2]: " -n 1 -r
echo

if [[ $REPLY =~ ^[2]$ ]]; then
    COMPOSE_FILE="docker-compose.yml"
    echo "Using original setup..."
else
    COMPOSE_FILE="docker-compose-alternative.yml"
    echo "Using alternative setup (recommended)..."
fi

# Clean up LocalStack if it's causing issues
cleanup_localstack

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down --remove-orphans 2>/dev/null || true

# Build and start all services
echo "🏗️ Building and starting services..."
docker-compose -f $COMPOSE_FILE up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."

echo "Waiting for database..."
timeout 60 bash -c "until docker-compose -f $COMPOSE_FILE exec -T db pg_isready -U postgres; do sleep 2; done"

echo "Waiting for LocalStack..."
timeout 120 bash -c "until curl -s http://localhost:4566/health > /dev/null; do sleep 2; done"

if [[ $COMPOSE_FILE == "docker-compose-alternative.yml" ]]; then
    echo "Waiting for Terraform to complete..."
    timeout 180 bash -c "until docker-compose -f $COMPOSE_FILE logs terraform | grep -q 'Infrastructure setup completed'; do sleep 5; done"
fi

echo "Waiting for backend..."
timeout 120 bash -c "until curl -s http://localhost:8000/api/products/ > /dev/null; do sleep 2; done"

echo "Waiting for frontend..."
timeout 60 bash -c "until curl -s http://localhost:3000 > /dev/null; do sleep 2; done"

echo ""
echo "🎉 Amigurumi Store is now running!"
echo "=================================="
echo ""
echo "📱 Frontend:     http://localhost:3000"
echo "🔧 Backend API:  http://localhost:8000/api/products/"
echo "👤 Django Admin: http://localhost:8000/admin/ (admin/admin123)"
echo "🗄️ Database:    localhost:5432 (postgres/postgres)"
echo "☁️ LocalStack:  http://localhost:4566"
echo ""
echo "📋 Available commands:"
echo "  docker-compose -f $COMPOSE_FILE logs -f [service]  # View logs"
echo "  docker-compose -f $COMPOSE_FILE stop              # Stop services"
echo "  docker-compose -f $COMPOSE_FILE down              # Stop and remove containers"
echo "  docker-compose -f $COMPOSE_FILE restart [service] # Restart a service"
echo ""
echo "🔍 Service status:"
docker-compose -f $COMPOSE_FILE ps
