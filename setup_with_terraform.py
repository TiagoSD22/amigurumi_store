"""
Alternative setup using Terraform for S3 bucket creation.
This approach is more reliable and follows infrastructure as code principles.
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def run_command(command, description, cwd=None, check=True):
    """Run a command and handle output."""
    print(f"\n{description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, 
                                  cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, 
                                  cwd=cwd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            if result.stdout and result.stdout.strip():
                # Print only the last few lines to avoid spam
                output_lines = result.stdout.strip().split('\n')
                if len(output_lines) > 5:
                    print("...")
                    for line in output_lines[-3:]:
                        print(line)
                else:
                    print(result.stdout.strip())
        else:
            print(f"✗ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
        
        return result.returncode == 0, result
    except Exception as e:
        print(f"✗ {description} failed with exception: {e}")
        return False, None

def check_docker():
    """Check if Docker is running."""
    success, result = run_command(['docker', 'ps'], "Check Docker status")
    if not success:
        print("Please make sure Docker Desktop is installed and running.")
        return False
    return True

def check_terraform():
    """Check if Terraform is installed."""
    success, result = run_command(['terraform', 'version'], "Check Terraform")
    if not success:
        print("Please install Terraform from: https://www.terraform.io/downloads")
        return False
    return True

def start_localstack():
    """Start LocalStack using Docker Compose or direct command."""
    print("\nStarting LocalStack...")
    
    # Try to stop any existing LocalStack
    run_command(['docker', 'stop', 'localstack_main'], "Stop existing LocalStack", check=False)
    
    # Start LocalStack with Docker
    success, result = run_command([
        'docker', 'run', '-d', 
        '--name', 'localstack_main',
        '-p', '4566:4566',
        '-e', 'SERVICES=s3',
        '-e', 'DEBUG=0',
        'localstack/localstack:latest'
    ], "Start LocalStack container", check=False)
    
    if not success:
        # Try alternative method
        run_command(['docker', 'rm', 'localstack_main'], "Remove existing container", check=False)
        success, result = run_command([
            'docker', 'run', '-d', 
            '--name', 'localstack_main',
            '-p', '4566:4566',
            '-e', 'SERVICES=s3',
            'localstack/localstack:latest'
        ], "Start LocalStack container (retry)")
    
    if success:
        print("Waiting for LocalStack to be ready...")
        time.sleep(15)
        
        # Test if LocalStack is responding
        for attempt in range(10):
            success, result = run_command([
                'curl', '-s', 'http://localhost:4566/health'
            ], f"Test LocalStack health (attempt {attempt + 1})", check=False)
            
            if success:
                print("✓ LocalStack is ready!")
                return True
            
            time.sleep(3)
        
        print("⚠️ LocalStack may not be fully ready, but continuing...")
        return True
    
    return False

def setup_terraform():
    """Initialize and apply Terraform configuration."""
    terraform_dir = Path(__file__).parent / 'terraform'
    
    if not terraform_dir.exists():
        print("✗ Terraform directory not found!")
        return False
    
    # Initialize Terraform
    success, result = run_command(['terraform', 'init'], "Initialize Terraform", cwd=terraform_dir)
    if not success:
        return False
    
    # Plan Terraform
    success, result = run_command(['terraform', 'plan'], "Plan Terraform changes", cwd=terraform_dir)
    if not success:
        return False
    
    # Apply Terraform
    success, result = run_command(['terraform', 'apply', '-auto-approve'], "Apply Terraform configuration", cwd=terraform_dir)
    if not success:
        return False
    
    return True

def setup_django():
    """Setup Django and run migrations."""
    backend_dir = Path(__file__).parent / 'backend'
    
    # Set DJANGO_SETTINGS_MODULE environment variable
    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
    
    # Run migrations
    success, result = run_command(
        [sys.executable, 'manage.py', 'migrate'],
        "Run Django migrations",
        cwd=backend_dir
    )
    
    return success

def main():
    """Main setup function using Terraform."""
    print("Amigurumi Store - Terraform + LocalStack Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_docker():
        return False
    
    if not check_terraform():
        return False
    
    # Start LocalStack
    if not start_localstack():
        print("\n❌ Failed to start LocalStack.")
        return False
    
    # Setup infrastructure with Terraform
    if not setup_terraform():
        print("\n❌ Failed to setup infrastructure with Terraform.")
        return False
    
    # Setup Django
    if not setup_django():
        print("\n❌ Failed to setup Django.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Infrastructure setup completed!")
    print("\nNext steps:")
    print("1. Run the migration script:")
    print(f"   python migrate_images_to_s3.py")
    print("\n2. Start the Django server:")
    print(f"   cd backend && python manage.py runserver")
    print("\n3. Start the React frontend:")
    print("   cd frontend && npm start")
    print("\n4. Visit http://localhost:3000 to see your store!")
    print("\nLocalStack S3 service is running on: http://localhost:4566")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("- Make sure Docker Desktop is running")
        print("- Make sure Terraform is installed")
        print("- Try running: docker pull localstack/localstack:latest")
        sys.exit(1)
