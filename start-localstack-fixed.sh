#!/bin/bash
set -e

echo "🚀 Starting Amigurumi Store with LocalStack S3..."

# Step 1: Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null || true

# Step 2: Remove any problematic images
echo "🗑️ Removing old images..."
docker image rm -f amigurumi_store-localstack 2>/dev/null || true
docker image rm -f amigurumi_store-backend 2>/dev/null || true
docker image rm -f amigurumi_store-frontend 2>/dev/null || true

# Step 3: Build and start services in correct order
echo "🏗️ Building and starting infrastructure services..."
docker-compose up -d --build db localstack

# Step 4: Wait for LocalStack to be ready
echo "⏳ Waiting for LocalStack to be ready..."
max_retries=60
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if docker-compose exec -T localstack curl -f http://localhost.localstack.cloud:4566/health > /dev/null 2>&1; then
        echo "✅ LocalStack is ready!"
        break
    fi
    echo "⏳ Waiting for LocalStack... (attempt $((retry_count + 1))/$max_retries)"
    sleep 5
    retry_count=$((retry_count + 1))
done

if [ $retry_count -eq $max_retries ]; then
    echo "❌ LocalStack failed to start within timeout"
    echo "📋 LocalStack logs:"
    docker-compose logs localstack
    exit 1
fi

# Step 5: Initialize infrastructure
echo "🔧 Initializing infrastructure with Terraform..."
docker-compose up --build terraform-init

# Step 6: Verify S3 bucket creation
echo "🧪 Verifying S3 infrastructure..."
docker-compose exec -T localstack aws --endpoint-url=http://localhost.localstack.cloud:4566 s3 ls

# Step 7: Start backend and frontend
echo "🚀 Starting backend and frontend services..."
docker-compose up -d --build backend frontend

# Step 8: Wait for all services to be healthy
echo "⏳ Waiting for all services to be healthy..."
sleep 30

# Step 9: Show service status
echo "📊 Service status:"
docker-compose ps

# Step 10: Test connectivity
echo "🧪 Testing service connectivity..."

# Test LocalStack
echo "🔍 Testing LocalStack..."
if curl -f http://localhost.localstack.cloud:4566/health > /dev/null 2>&1; then
    echo "✅ LocalStack is accessible"
else
    echo "❌ LocalStack is not accessible"
fi

# Test Backend
echo "🔍 Testing Backend..."
if curl -f http://localhost:8000/api/products/ > /dev/null 2>&1; then
    echo "✅ Backend API is accessible"
else
    echo "❌ Backend API is not accessible"
fi

# Test Frontend
echo "🔍 Testing Frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "🎉 Startup complete!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api/"
echo "   Django Admin: http://localhost:8000/admin/ (admin/admin123)"
echo "   LocalStack: http://localhost.localstack.cloud:4566"
echo ""
echo "🔧 To check logs:"
echo "   docker-compose logs [service_name]"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"
echo ""
