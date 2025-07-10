#!/bin/bash
set -e

echo "🚀 Initializing LocalStack infrastructure..."

# Set AWS CLI configuration for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566

# Configure AWS CLI for LocalStack
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set default.region us-east-1
aws configure set default.s3.signature_version s3v4
aws configure set default.s3.addressing_style path



# Initialize Terraform
cd /terraform
echo "🔧 Initializing Terraform..."
terraform init

echo "📋 Planning Terraform changes..."
terraform plan

echo "🚀 Applying Terraform configuration..."
terraform apply -auto-approve

echo "✅ Infrastructure setup completed!"



echo "🎉 LocalStack initialization complete!"

echo "🎉 LocalStack infrastructure is ready!"
