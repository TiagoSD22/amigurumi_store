"""
Script to migrate sample images to S3 bucket and create products in Django database.
This script assumes LocalStack is running on localhost.localstack.cloud:4566.
"""

import os
import boto3
import django
from pathlib import Path
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amigurumi_store.settings')
django.setup()

from products.models import AmigurumiProduct

# S3 Configuration for LocalStack
S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', 'http://localhost:4566')
S3_BUCKET_NAME = 'product-image-collection'
AWS_ACCESS_KEY_ID = 'test'
AWS_SECRET_ACCESS_KEY = 'test'
AWS_REGION = 'us-east-1'

# Product data for each sample image
PRODUCT_DATA = {
    'sample_1.jpg': {
        'name': 'Adorable Bunny',
        'description': 'A cute and cuddly bunny amigurumi perfect for children and collectors. Made with soft cotton yarn in beautiful pastel colors.',
        'price': 25.99,
        'category': 'ANIMAL',
        'is_available': True,
    },
    'sample_2.jpg': {
        'name': 'Rainbow Unicorn',
        'description': 'Magical rainbow unicorn with sparkling horn and flowing mane. A perfect gift for unicorn lovers of all ages.',
        'price': 32.99,
        'category': 'CHARACTER',
        'is_available': True,
    },
    'sample_3.jpg': {
        'name': 'Cozy Bear',
        'description': 'A warm and huggable teddy bear made with premium wool yarn. Perfect companion for bedtime stories.',
        'price': 28.50,
        'category': 'ANIMAL',
        'is_available': True,
    },
    'sample_4.jpg': {
        'name': 'Ocean Octopus',
        'description': 'Friendly eight-armed octopus in vibrant ocean colors. Each tentacle is perfectly crafted for endless play.',
        'price': 22.75,
        'category': 'ANIMAL',
        'is_available': True,
    },
    'sample_5.jpg': {
        'name': 'Garden Flower',
        'description': 'Beautiful sunflower with detailed petals and leaves. Brings the joy of spring into any room.',
        'price': 18.99,
        'category': 'ACCESSORIES',
        'is_available': True,
    },
    'sample_6.jpg': {
        'name': 'Space Alien',
        'description': 'Cute extraterrestrial friend with big eyes and antenna. Perfect for space enthusiasts and sci-fi fans.',
        'price': 24.99,
        'category': 'CHARACTER',
        'is_available': True,
    },
    'sample_7.jpg': {
        'name': 'Christmas Elf',
        'description': 'Festive holiday elf with pointed hat and jingle bells. Seasonal decoration that brings Christmas magic.',
        'price': 26.50,
        'category': 'SEASONAL',
        'is_available': True,
    },
    'sample_8.jpg': {
        'name': 'Desert Cactus',
        'description': 'Adorable cactus with a flower crown. Low-maintenance decoration that adds charm to any space.',
        'price': 16.99,
        'category': 'ACCESSORIES',
        'is_available': True,
    },
    'sample_9.jpg': {
        'name': 'Forest Fox',
        'description': 'Clever woodland fox with bushy tail and alert ears. Handcrafted with attention to every detail.',
        'price': 30.25,
        'category': 'ANIMAL',
        'is_available': True,
    },
    'sample_10.jpg': {
        'name': 'Dragon Guardian',
        'description': 'Majestic dragon with detailed scales and wings. A powerful protector for any amigurumi collection.',
        'price': 45.99,
        'category': 'CHARACTER',
        'is_available': True,
    },
    'sample_11.jpg': {
        'name': 'Birthday Cake',
        'description': 'Celebratory birthday cake with candles and frosting details. Perfect for party decorations and gifts.',
        'price': 21.50,
        'category': 'ACCESSORIES',
        'is_available': True,
    },
}

def create_s3_client():
    """Create and configure S3 client for LocalStack."""
    from botocore.config import Config
    
    # Configuration for LocalStack compatibility
    config = Config(
        region_name=AWS_REGION,
        signature_version='s3v4',
        s3={
            'addressing_style': 'path'
        }
    )
    
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
        config=config,
        verify=False  # Disable SSL verification for LocalStack
    )

def check_bucket_exists(s3_client):
    """Check if the S3 bucket exists."""
    try:
        s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
        print(f"✓ Bucket '{S3_BUCKET_NAME}' exists")
        return True
    except Exception as e:
        print(f"✗ Bucket '{S3_BUCKET_NAME}' does not exist: {e}")
        return False

def upload_image_to_s3(s3_client, image_path, product_id):
    """Upload an image to S3 and return the S3 path."""
    try:
        # Create S3 key with product folder structure
        s3_key = f"products/{product_id}/{os.path.basename(image_path)}"
        
        # Upload file
        with open(image_path, 'rb') as file:
            s3_client.upload_fileobj(
                file,
                S3_BUCKET_NAME,
                s3_key,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
        
        # Return the S3 path
        s3_path = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        print(f"✓ Uploaded {image_path} to {s3_path}")
        return s3_path
        
    except Exception as e:
        print(f"✗ Failed to upload {image_path}: {e}")
        return None

def create_or_update_product(image_filename, s3_path, product_data):
    """Create or update a product in the database."""
    try:
        # Extract product ID from filename (e.g., 'sample_1.jpg' -> 1)
        product_id = int(image_filename.split('_')[1].split('.')[0])
        
        # Create or update product
        product, created = AmigurumiProduct.objects.update_or_create(
            id=product_id,
            defaults={
                'name': product_data['name'],
                'description': product_data['description'],
                'price': product_data['price'],
                'category': product_data['category'],
                'image_s3_path': os.path.basename(image_filename),  # Just store filename
                'is_available': product_data['is_available'],
            }
        )
        
        action = "Created" if created else "Updated"
        print(f"✓ {action} product: {product.name} (ID: {product.id})")
        return product
        
    except Exception as e:
        print(f"✗ Failed to create/update product for {image_filename}: {e}")
        return None

def main():
    """Main migration function."""
    print("Starting S3 migration and database population...")
    print("=" * 50)
    
    # Initialize S3 client
    s3_client = create_s3_client()
    
    # Check if bucket exists
    if not check_bucket_exists(s3_client):
        print("Please ensure LocalStack is running and the S3 bucket is created via Terraform.")
        return
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Process each image
    successful_uploads = 0
    successful_products = 0
    
    for image_filename, product_data in PRODUCT_DATA.items():
        image_path = current_dir / image_filename
        
        if not image_path.exists():
            print(f"✗ Image file not found: {image_path}")
            continue
        
        # Extract product ID for folder structure
        product_id = int(image_filename.split('_')[1].split('.')[0])
        
        # Upload image to S3
        s3_path = upload_image_to_s3(s3_client, str(image_path), product_id)
        
        if s3_path:
            successful_uploads += 1
            
            # Create/update product in database
            product = create_or_update_product(image_filename, s3_path, product_data)
            
            if product:
                successful_products += 1
    
    # Summary
    print("=" * 50)
    print(f"Migration completed!")
    print(f"✓ Successfully uploaded {successful_uploads}/{len(PRODUCT_DATA)} images to S3")
    print(f"✓ Successfully created/updated {successful_products}/{len(PRODUCT_DATA)} products")
    
    if successful_products == len(PRODUCT_DATA):
        print("\n🎉 All products successfully migrated to S3!")
        print("\nNext steps:")
        print("1. Start the Django development server: python backend/manage.py runserver")
        print("2. Start the React frontend: cd frontend && npm start")
        print("3. Visit http://localhost:3000 to see your amigurumi store!")
    else:
        print(f"\n⚠️  Some products failed to migrate. Please check the errors above.")

if __name__ == "__main__":
    main()
