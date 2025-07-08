"""
Create S3 bucket in LocalStack after it's running.
Run this after LocalStack has started successfully.
"""

import boto3
import json
import sys
import time

def test_localstack_connection():
    """Test if LocalStack is accessible."""
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:4566/health', timeout=5)
        health_data = response.read().decode('utf-8')
        print(f"✅ LocalStack health check: {health_data}")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to LocalStack: {e}")
        print("Make sure LocalStack is running with: python start_localstack_host.py")
        return False

def create_s3_bucket():
    """Create and configure the S3 bucket."""
    try:
        print("🪣 Creating S3 bucket...")
        
        # Create S3 client
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1',
        )
        
        bucket_name = 'product-image-collection'
        
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' already exists")
        except:
            # Create bucket
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"✅ Created bucket '{bucket_name}'")
        
        # Set bucket policy for public read access
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(policy)
        )
        print("✅ Set bucket policy for public read access")
        
        # Test bucket access
        buckets = s3_client.list_buckets()
        print(f"✅ Available buckets: {[b['Name'] for b in buckets['Buckets']]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create S3 bucket: {e}")
        return False

def main():
    """Main function."""
    print("🎯 S3 Bucket Creation for Amigurumi Store")
    print("=" * 45)
    
    # Test LocalStack connection
    if not test_localstack_connection():
        return False
    
    # Create S3 bucket
    if not create_s3_bucket():
        return False
    
    print("\n🎉 S3 bucket setup completed!")
    print("\nNext steps:")
    print("1. Run: python migrate_images_to_s3.py")
    print("2. Start Django: cd backend && python manage.py runserver")
    print("3. Start React: cd frontend && npm start")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ S3 bucket setup failed.")
        print("Check that LocalStack is running properly.")
        sys.exit(1)
