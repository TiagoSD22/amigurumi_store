"""
Simple script to populate the database with sample products
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))
django.setup()

from products.models import AmigurumiProduct
from decimal import Decimal

def create_sample_products():
    """Create sample products"""
    print("Creating sample products...")
    
    # Clear existing products
    AmigurumiProduct.objects.all().delete()
    
    # Sample product data
    products = [
        {
            'name': 'Adorable Orange Fox Amigurumi',
            'description': 'Handcrafted orange fox with white details. Perfect for children and fox lovers. Made with soft cotton yarn.',
            'price': Decimal('45.00'),
            'category': 'ANIMAL',
            'is_featured': True,
        },
        {
            'name': 'Sweet Green Teddy Bear',
            'description': 'Lovely green teddy bear with embroidered features. Soft and cuddly, perfect for babies and children.',
            'price': Decimal('38.00'),
            'category': 'ANIMAL',
            'is_featured': True,
        },
        {
            'name': 'Blue Lace Doily Set',
            'description': 'Beautiful handcrafted blue and white lace doily. Perfect for home decoration and table settings.',
            'price': Decimal('25.00'),
            'category': 'ACCESSORIES',
            'is_featured': False,
        },
        {
            'name': 'Blue Triangle Shawl',
            'description': 'Elegant blue crocheted shawl with intricate patterns. Perfect for special occasions.',
            'price': Decimal('65.00'),
            'category': 'ACCESSORIES',
            'is_featured': False,
        },
        {
            'name': 'Pink Wool Sheep',
            'description': 'Cute pink sheep amigurumi with textured wool-like body. Adorable addition to any collection.',
            'price': Decimal('42.00'),
            'category': 'ANIMAL',
            'is_featured': True,
        },
        {
            'name': 'Rainbow Unicorn Princess',
            'description': 'Magical white unicorn with rainbow mane and pink details. Every little princess will love it!',
            'price': Decimal('55.00'),
            'category': 'CHARACTER',
            'is_featured': True,
        }
    ]
    
    for product_data in products:
        product = AmigurumiProduct.objects.create(**product_data)
        print(f"✓ Created: {product.name}")
    
    print(f"✓ Created {AmigurumiProduct.objects.count()} sample products")

if __name__ == '__main__':
    create_sample_products()
    print("Sample data creation complete!")
