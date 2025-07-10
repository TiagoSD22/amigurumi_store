import argparse
import boto3
import os
import sys
from pathlib import Path
from typing import List

def get_s3_client(stack: str):
    """Get S3 client based on stack environment"""
    if stack == "local":
        # For localstack
        return boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
    else:
        # For AWS environments (demo, stage, prod)
        return boto3.client('s3')

def upload_image_to_s3(s3_client, bucket_name: str, product_id: int, image_path: str) -> bool:
    """Upload a single image to S3"""
    try:
        # Get the filename from the path
        filename = Path(image_path).name
        
        # Create the S3 key (path in bucket)
        s3_key = f"{product_id}/{filename}"
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Error: File {image_path} does not exist")
            return False
        
        # Upload the file
        s3_client.upload_file(image_path, bucket_name, s3_key)
        print(f"Successfully uploaded {image_path} to s3://{bucket_name}/{s3_key}")
        return True
        
    except Exception as e:
        print(f"Error uploading {image_path}: {str(e)}")
        return False

def create_bucket_if_not_exists(s3_client, bucket_name: str, stack: str):
    """Create bucket if it doesn't exist (mainly for localstack)"""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except s3_client.exceptions.NoSuchBucket:
        if stack == "local":
            try:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Created bucket {bucket_name}")
            except Exception as e:
                print(f"Error creating bucket {bucket_name}: {str(e)}")
                return False
        else:
            print(f"Error: Bucket {bucket_name} does not exist in {stack} environment")
            return False
    except Exception as e:
        print(f"Error checking bucket {bucket_name}: {str(e)}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Upload product images to S3 bucket')
    parser.add_argument('--stack', 
                       choices=['local', 'demo', 'stage', 'prod'],
                       default='local',
                       help='Stack environment (default: local)')
    parser.add_argument('--product_id', 
                       type=int,
                       required=True,
                       help='Product ID (numerical value)')
    parser.add_argument('--images', 
                       type=str,
                       required=True,
                       help='Space-separated list of image paths')
    
    args = parser.parse_args()
    
    # Parse the images argument (space-separated paths)
    image_paths = args.images.split()
    
    if not image_paths:
        print("Error: No images provided")
        sys.exit(1)
    
    # Validate that all image files exist
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Error: Image file {image_path} does not exist")
            sys.exit(1)
    
    bucket_name = "product-image-collection"
    
    print(f"Starting upload process...")
    print(f"Stack: {args.stack}")
    print(f"Product ID: {args.product_id}")
    print(f"Images to upload: {len(image_paths)}")
    print(f"Bucket: {bucket_name}")
    
    try:
        # Get S3 client
        s3_client = get_s3_client(args.stack)
        
        # Create bucket if it doesn't exist (mainly for localstack)
        if not create_bucket_if_not_exists(s3_client, bucket_name, args.stack):
            sys.exit(1)
        
        # Upload each image
        successful_uploads = 0
        failed_uploads = 0
        
        for image_path in image_paths:
            if upload_image_to_s3(s3_client, bucket_name, args.product_id, image_path):
                successful_uploads += 1
            else:
                failed_uploads += 1
        
        print(f"\nUpload complete!")
        print(f"Successful uploads: {successful_uploads}")
        print(f"Failed uploads: {failed_uploads}")
        
        if failed_uploads > 0:
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()