#!/usr/bin/env python3
"""
Test S3 connectivity for LocalStack integration
"""

import boto3
import os
import sys
from botocore.exceptions import ClientError, NoCredentialsError
from botocore.config import Config

def test_s3_connectivity():
    """Test S3 connectivity with LocalStack"""
    print("🧪 Testing S3 connectivity...")
    
    # Configuration for LocalStack
    endpoint_url = os.environ.get('AWS_S3_ENDPOINT_URL', 'http://localstack:4566')
    bucket_name = 'product-image-collection'
    
    # Configure boto3 client for LocalStack
    s3_config = Config(
        signature_version='s3v4',
        s3={
            'addressing_style': 'path'
        }
    )
    
    try:
        # Create S3 client
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1',
            config=s3_config,
            verify=False
        )
        
        print(f"✅ S3 client created successfully")
        print(f"📍 Endpoint: {endpoint_url}")
        
        # Test connection by listing buckets
        print("📋 Listing buckets...")
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print(f"✅ Found buckets: {buckets}")
        
        # Check if our bucket exists
        if bucket_name in buckets:
            print(f"✅ Bucket '{bucket_name}' exists")
            
            # Test bucket access
            print(f"🧪 Testing bucket access...")
            try:
                response = s3_client.list_objects_v2(Bucket=bucket_name)
                print(f"✅ Bucket access successful")
                print(f"📦 Objects in bucket: {response.get('KeyCount', 0)}")
            except ClientError as e:
                print(f"⚠️  Bucket access issue: {e}")
        else:
            print(f"❌ Bucket '{bucket_name}' not found")
            return False
            
        # Test upload capability
        print("🧪 Testing upload capability...")
        try:
            test_content = b"test file content"
            test_key = "test-file.txt"
            
            s3_client.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=test_content,
                ACL='public-read'
            )
            print(f"✅ Upload test successful")
            
            # Test download
            obj = s3_client.get_object(Bucket=bucket_name, Key=test_key)
            content = obj['Body'].read()
            if content == test_content:
                print(f"✅ Download test successful")
            else:
                print(f"❌ Download content mismatch")
                
            # Clean up test file
            s3_client.delete_object(Bucket=bucket_name, Key=test_key)
            print(f"✅ Test file cleaned up")
            
        except ClientError as e:
            print(f"❌ Upload/download test failed: {e}")
            return False
            
        print("🎉 All S3 connectivity tests passed!")
        return True
        
    except NoCredentialsError:
        print("❌ AWS credentials not found")
        return False
    except ClientError as e:
        print(f"❌ AWS client error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_s3_connectivity()
    sys.exit(0 if success else 1)
