#!/bin/bash

echo "🔍 Debugging LocalStack S3 connectivity..."

# Check if LocalStack container is running
echo "📦 Checking LocalStack container status..."
docker-compose ps localstack

# Check LocalStack health
echo "🏥 Checking LocalStack health..."
docker-compose exec -T localstack curl -s http://localhost:4566/health | jq . || echo "Health check failed"

# Check S3 service specifically
echo "🪣 Checking S3 service status..."
docker-compose exec -T localstack curl -s http://localhost:4566/health | grep -o '"s3":"[^"]*"' || echo "S3 status check failed"

# List S3 buckets
echo "📋 Listing S3 buckets..."
docker-compose exec -T localstack aws --endpoint-url=http://localhost:4566 s3 ls || echo "S3 bucket listing failed"

# Check if our bucket exists
echo "🎯 Checking specific bucket..."
docker-compose exec -T localstack aws --endpoint-url=http://localhost:4566 s3 ls s3://product-image-collection || echo "Bucket access failed"

# Test S3 connectivity from backend container
echo "🧪 Testing S3 from backend container..."
docker-compose exec -T backend python /app/scripts/test-s3-connectivity.py || echo "Backend S3 test failed"

# Check LocalStack logs
echo "📋 Recent LocalStack logs:"
docker-compose logs --tail=50 localstack

# Check backend logs for S3 errors
echo "📋 Recent backend logs (S3 related):"
docker-compose logs backend | grep -i s3 | tail -20 || echo "No S3-related backend logs"

echo "🔍 Debug complete!"
