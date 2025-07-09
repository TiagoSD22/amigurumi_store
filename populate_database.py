"""
Simplified migration script that creates products in Django database
without requiring S3/LocalStack for initial testing.
This can be used to populate the database with sample data.
"""

import os
import django
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from products.models import AmigurumiProduct

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

def create_or_update_product(image_filename, product_data):
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
                'image_s3_path': image_filename,  # Store filename for now
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
    print("Creating sample products in Django database...")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Process each image
    successful_products = 0
    
    for image_filename, product_data in PRODUCT_DATA.items():
        image_path = current_dir / image_filename
        
        if not image_path.exists():
            print(f"⚠️  Image file not found: {image_path} (continuing anyway)")
        
        # Create/update product in database
        product = create_or_update_product(image_filename, product_data)
        
        if product:
            successful_products += 1
    
    # Summary
    print("=" * 50)
    print(f"Database population completed!")
    print(f"✓ Successfully created/updated {successful_products}/{len(PRODUCT_DATA)} products")
    
    if successful_products == len(PRODUCT_DATA):
        print("\n🎉 All products successfully created in database!")
        print("\nYou can now:")
        print("1. Start the Django development server:")
        print("   cd backend && python manage.py runserver")
        print("2. Visit http://127.0.0.1:8000/api/products/ to see the API")
        print("3. Start the React frontend:")
        print("   cd frontend && npm start")
        print("4. Visit http://localhost:3000 to see your amigurumi store!")
        print("\nNote: Images will show placeholder until S3 is configured.")
    else:
        print(f"\n⚠️  Some products failed to be created. Please check the errors above.")

if __name__ == "__main__":
    main()
