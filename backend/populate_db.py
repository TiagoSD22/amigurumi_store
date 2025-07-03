"""
Script to populate the database with sample amigurumi products
Run this after running migrations
"""

import os
import django
import sys
from pathlib import Path

# Add the parent directory to the path so we can import Django modules
sys.path.append(str(Path(__file__).resolve().parent))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amigurumi_store.settings')
django.setup()

from products.models import AmigurumiProduct
from django.core.files import File
from decimal import Decimal

def populate_products():
    """Create sample products with the uploaded images"""
    
    # Sample product data based on the images provided
    products_data = [
        {
            'name': 'Adorable Orange Fox Amigurumi',
            'description': 'Handcrafted orange fox with white details. Perfect for children and fox lovers. Made with soft cotton yarn.',
            'price': Decimal('45.00'),
            'category': 'ANIMAL',
            'image_file': 'sample_1.jpg',
            'is_featured': True,
        },
        {
            'name': 'Sweet Green Teddy Bear',
            'description': 'Lovely green teddy bear with embroidered features. Soft and cuddly, perfect for babies and children.',
            'price': Decimal('38.00'),
            'category': 'ANIMAL',
            'image_file': 'sample_2.jpg',
            'is_featured': True,
        },
        {
            'name': 'Blue Lace Doily Set',
            'description': 'Beautiful handcrafted blue and white lace doily. Perfect for home decoration and table settings.',
            'price': Decimal('25.00'),
            'category': 'ACCESSORIES',
            'image_file': 'sample_3.jpg',
            'is_featured': False,
        },
        {
            'name': 'Blue Triangle Shawl',
            'description': 'Elegant blue crocheted shawl with intricate patterns. Perfect for special occasions.',
            'price': Decimal('65.00'),
            'category': 'ACCESSORIES',
            'image_file': 'sample_4.jpg',
            'is_featured': False,
        },
        {
            'name': 'Pink Wool Sheep',
            'description': 'Cute pink sheep amigurumi with textured wool-like body. Adorable addition to any collection.',
            'price': Decimal('42.00'),
            'category': 'ANIMAL',
            'image_file': 'sample_5.jpg',
            'is_featured': True,
        },
        {
            'name': 'Rainbow Unicorn Princess',
            'description': 'Magical white unicorn with rainbow mane and pink details. Every little princess will love it!',
            'price': Decimal('55.00'),
            'category': 'CHARACTER',
            'image_file': 'sample_6.jpg',
            'is_featured': True,
        },
        {
            'name': 'Little Blonde Girl Doll',
            'description': 'Charming little girl doll with blonde hair and green dress. Handmade with love and attention to detail.',
            'price': Decimal('48.00'),
            'category': 'DOLL',
            'image_file': 'sample_7.jpg',
            'is_featured': False,
        },
        {
            'name': 'Pink Bunny Ballerina',
            'description': 'Elegant pink bunny in a beautiful orange tutu dress. Perfect for dance lovers!',
            'price': Decimal('52.00'),
            'category': 'ANIMAL',
            'image_file': 'sample_8.jpg',
            'is_featured': True,
        },
        {
            'name': 'Winter Penguin with Scarf',
            'description': 'Adorable black and white penguin wearing a blue winter scarf and hat. Perfect for winter decor.',
            'price': Decimal('40.00'),
            'category': 'SEASONAL',
            'image_file': 'sample_9.jpg',
            'is_featured': False,
        },
        {
            'name': 'Colorful Rainbow Unicorn',
            'description': 'Majestic white unicorn with vibrant rainbow mane and pink hooves. A magical friend for all ages.',
            'price': Decimal('58.00'),
            'category': 'CHARACTER',
            'image_file': 'sample_10.jpg',
            'is_featured': True,
        },
        {
            'name': 'Pink Flower Coaster Set',
            'description': 'Beautiful set of pink crocheted flower coasters. Perfect for protecting your furniture in style.',
            'price': Decimal('28.00'),
            'category': 'ACCESSORIES',
            'image_file': 'sample_11.jpg',
            'is_featured': False,
        },
    ]
    
    # Clear existing products
    AmigurumiProduct.objects.all().delete()
    
    media_dir = Path(__file__).resolve().parent / 'media' / 'amigurumi'
    
    for product_data in products_data:
        image_path = media_dir / product_data['image_file']
        
        if image_path.exists():
            product = AmigurumiProduct(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=product_data['category'],
                is_featured=product_data['is_featured'],
                is_available=True
            )
            
            # Copy the image file to the product
            with open(image_path, 'rb') as img_file:
                product.image.save(
                    product_data['image_file'],
                    File(img_file),
                    save=False
                )
            
            product.save()
            print(f"Created product: {product.name}")
        else:
            print(f"Image not found: {image_path}")
    
    print(f"Created {AmigurumiProduct.objects.count()} products")

if __name__ == '__main__':
    populate_products()
