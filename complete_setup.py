"""
Complete setup script for the Amigurumi Store S3 migration.
This script will:
1. Start LocalStack
2. Create S3 bucket
3. Upload images to S3
4. Populate Django database
5. Provide next steps
"""

import subprocess
import time
import sys
import os
from pathlib import Path
import json

def run_command(command, description, check=True, capture_output=True):
    """Run a command and handle output."""
    print(f"\n{description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=capture_output, text=True)
        else:
            result = subprocess.run(command, check=check, 
                                  capture_output=capture_output, text=True)
        
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            if result.stdout and result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"✗ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
        
        return result.returncode == 0, result
    except Exception as e:
        print(f"✗ {description} failed with exception: {e}")
        return False, None

def check_prerequisites():
    """Check if all prerequisites are installed."""
    print("Checking prerequisites...")
    
    # Check Python
    success, result = run_command([sys.executable, '--version'], "Check Python version")
    if not success:
        return False
    
    # Check pip
    success, result = run_command([sys.executable, '-m', 'pip', '--version'], "Check pip")
    if not success:
        return False
    
    # Check Docker
    success, result = run_command(['docker', '--version'], "Check Docker")
    if not success:
        print("Please install Docker Desktop and make sure it's running.")
        return False
    
    # Check if Docker is running
    success, result = run_command(['docker', 'ps'], "Check if Docker is running")
    if not success:
        print("Please start Docker Desktop.")
        return False
    
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\nInstalling Python dependencies...")
    
    # Install from requirements.txt
    requirements_path = Path(__file__).parent / 'backend' / 'requirements.txt'
    if requirements_path.exists():
        success, result = run_command(
            [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)],
            "Install backend requirements"
        )
        if not success:
            return False
    else:
        # Install individual packages
        packages = [
            'Django==4.2.7',
            'djangorestframework==3.14.0', 
            'django-cors-headers==4.3.1',
            'Pillow==10.1.0',
            'boto3==1.34.0',
            'localstack==3.0.0'
        ]
        
        for package in packages:
            success, result = run_command(
                [sys.executable, '-m', 'pip', 'install', package],
                f"Install {package}"
            )
            if not success:
                return False
    
    return True

def start_localstack():
    """Start LocalStack and wait for it to be ready."""
    print("\nStarting LocalStack...")
    
    # Kill any existing LocalStack processes
    run_command(['localstack', 'stop'], "Stop existing LocalStack", check=False)
    time.sleep(2)
    
    # Start LocalStack
    env = os.environ.copy()
    env['SERVICES'] = 's3'
    env['DEBUG'] = '0'
    
    try:
        # Start LocalStack in background
        process = subprocess.Popen(
            ['localstack', 'start'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("Waiting for LocalStack to start (this may take 30-60 seconds)...")
        
        # Wait and check if LocalStack is ready
        max_attempts = 12
        for attempt in range(max_attempts):
            time.sleep(5)
            try:
                # Test if LocalStack is responding
                result = subprocess.run(
                    ['curl', '-s', 'http://localhost:4566/health'],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    print("✓ LocalStack is ready!")
                    return True
            except:
                pass
            
            print(f"Attempt {attempt + 1}/{max_attempts}: Still waiting...")
        
        print("✗ LocalStack failed to start within expected time")
        return False
        
    except Exception as e:
        print(f"✗ Failed to start LocalStack: {e}")
        return False

def create_s3_bucket():
    """Create S3 bucket using AWS CLI or boto3."""
    print("\nCreating S3 bucket...")
    
    # Try using AWS CLI first (simpler)
    success, result = run_command([
        'aws', '--endpoint-url=http://localhost:4566',
        's3', 'mb', 's3://product-image-collection'
    ], "Create S3 bucket with AWS CLI", check=False)
    
    if success:
        # Set public read policy
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::product-image-collection/*"
                }
            ]
        }
        
        # Write policy to temp file
        policy_file = Path(__file__).parent / 'temp_policy.json'
        with open(policy_file, 'w') as f:
            json.dump(policy, f)
        
        success, result = run_command([
            'aws', '--endpoint-url=http://localhost:4566',
            's3api', 'put-bucket-policy',
            '--bucket', 'product-image-collection',
            '--policy', f'file://{policy_file}'
        ], "Set bucket policy", check=False)
        
        # Clean up temp file
        if policy_file.exists():
            policy_file.unlink()
        
        return True
    
    # If AWS CLI failed, try with Python
    print("AWS CLI not available, using Python boto3...")
    
    try:
        import boto3
        
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1',
        )
        
        # Create bucket
        s3_client.create_bucket(Bucket='product-image-collection')
        
        # Set policy
        s3_client.put_bucket_policy(
            Bucket='product-image-collection',
            Policy=json.dumps(policy)
        )
        
        print("✓ S3 bucket created successfully with Python")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create S3 bucket: {e}")
        return False

def setup_django():
    """Set up Django database and run migrations."""
    print("\nSetting up Django...")
    
    backend_dir = Path(__file__).parent / 'backend'
    
    # Run migrations
    success, result = run_command(
        [sys.executable, 'manage.py', 'migrate'],
        "Run Django migrations",
        capture_output=False
    )
    if not success:
        return False
    
    return True

def main():
    """Main setup function."""
    print("Amigurumi Store - Complete S3 Migration Setup")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please resolve the issues above.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies.")
        return False
    
    # Start LocalStack
    if not start_localstack():
        print("\n❌ Failed to start LocalStack.")
        print("You can try starting it manually with: localstack start")
        return False
    
    # Create S3 bucket
    if not create_s3_bucket():
        print("\n❌ Failed to create S3 bucket.")
        return False
    
    # Setup Django
    if not setup_django():
        print("\n❌ Failed to setup Django.")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the migration script:")
    print(f"   {sys.executable} migrate_images_to_s3.py")
    print("\n2. Start the Django server:")
    print(f"   cd backend && {sys.executable} manage.py runserver")
    print("\n3. Start the React frontend:")
    print("   cd frontend && npm start")
    print("\n4. Visit http://localhost:3000 to see your store!")
    print("\nNote: Keep LocalStack running in a separate terminal.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
