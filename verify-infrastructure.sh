#!/bin/bash

echo "🔍 Checking LocalStack S3 infrastructure..."

# Check if LocalStack is running
if ! curl -s http://localhost:4566/health > /dev/null; then
    echo "❌ LocalStack is not running on http://localhost:4566"
    exit 1
fi

echo "✅ LocalStack is running"

# Check if S3 service is available
echo "📦 Checking S3 service..."
if ! curl -s http://localhost:4566/health | grep -q '"s3": "available"' 2>/dev/null; then
    echo "⚠️  S3 service might not be fully ready yet"
fi

# List S3 buckets
echo "🪣 Listing S3 buckets:"
aws --endpoint-url=http://localhost:4566 s3 ls 2>/dev/null || echo "Failed to list buckets"

# Check for our specific bucket
echo "🔍 Checking for 'product-image-collection' bucket:"
if aws --endpoint-url=http://localhost:4566 s3 ls s3://product-image-collection 2>/dev/null; then
    echo "✅ Bucket 'product-image-collection' exists!"
else
    echo "❌ Bucket 'product-image-collection' not found!"
    echo ""
    echo "🔧 Creating bucket manually..."
    aws --endpoint-url=http://localhost:4566 s3 mb s3://product-image-collection
    
    if [ $? -eq 0 ]; then
        echo "✅ Bucket created successfully!"
    else
        echo "❌ Failed to create bucket"
        exit 1
    fi
fi

echo ""
echo "🎉 Infrastructure verification completed!"
