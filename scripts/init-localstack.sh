#!/bin/bash
set -e

echo "🚀 Initializing LocalStack infrastructure..."

# Wait for LocalStack to be fully ready
echo "⏳ Waiting for LocalStack to be ready..."
sleep 5

# Test LocalStack connectivity
echo "🔍 Testing LocalStack connectivity..."
max_retries=30
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if curl -f http://localhost:4566/health > /dev/null 2>&1; then
        echo "✅ LocalStack is ready!"
        break
    fi
    echo "⏳ Waiting for LocalStack... (attempt $((retry_count + 1))/$max_retries)"
    sleep 2
    retry_count=$((retry_count + 1))
done

if [ $retry_count -eq $max_retries ]; then
    echo "❌ LocalStack failed to start within timeout"
    exit 1
fi

# Set AWS CLI configuration for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566

# Configure AWS CLI for LocalStack
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set default.region us-east-1
aws configure set default.s3.signature_version s3v4
aws configure set default.s3.addressing_style path

# Test S3 service
echo "🧪 Testing S3 service..."
aws --endpoint-url=http://localhost:4566 s3 ls || echo "S3 not yet ready, continuing..."

# Initialize Terraform
cd /terraform
echo "🔧 Initializing Terraform..."
terraform init

echo "📋 Planning Terraform changes..."
terraform plan

echo "🚀 Applying Terraform configuration..."
terraform apply -auto-approve

echo "✅ Infrastructure setup completed!"

# Verify created resources
echo "📝 Verifying created resources:"
aws --endpoint-url=http://localhost:4566 s3 ls

# Test bucket access
echo "🧪 Testing bucket access..."
aws --endpoint-url=http://localhost:4566 s3 ls s3://product-image-collection || echo "Bucket not accessible yet"

echo "🎉 LocalStack initialization complete!"

echo "🎉 LocalStack infrastructure is ready!"
