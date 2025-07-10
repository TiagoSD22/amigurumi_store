from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from products.models import AmigurumiProduct
from products.services import S3ImageService
import os
import glob

class Command(BaseCommand):
    help = 'Upload product images to S3 and clear image cache'

    def add_arguments(self, parser):
        parser.add_argument(
            '--product-id',
            type=int,
            help='Product ID to upload images for'
        )
        parser.add_argument(
            '--image-dir',
            type=str,
            help='Directory containing images to upload'
        )
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Clear image cache for all products'
        )

    def handle(self, *args, **options):
        s3_service = S3ImageService()

        if options['clear_cache']:
            self.stdout.write('Clearing image cache for all products...')
            products = AmigurumiProduct.objects.all()
            for product in products:
                product.invalidate_image_cache()
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared cache for all products')
            )
            return

        if options['product_id'] and options['image_dir']:
            product_id = options['product_id']
            image_dir = options['image_dir']
            
            try:
                product = AmigurumiProduct.objects.get(id=product_id)
            except AmigurumiProduct.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Product with ID {product_id} does not exist')
                )
                return

            if not os.path.exists(image_dir):
                self.stdout.write(
                    self.style.ERROR(f'Directory {image_dir} does not exist')
                )
                return

            # Find all image files in the directory
            image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
            image_files = []
            
            for extension in image_extensions:
                pattern = os.path.join(image_dir, extension)
                image_files.extend(glob.glob(pattern))
                # Also check uppercase extensions
                pattern = os.path.join(image_dir, extension.upper())
                image_files.extend(glob.glob(pattern))

            if not image_files:
                self.stdout.write(
                    self.style.WARNING(f'No image files found in {image_dir}')
                )
                return

            self.stdout.write(
                f'Found {len(image_files)} image files for product {product.name}'
            )

            successful_uploads = 0
            failed_uploads = 0

            for image_path in image_files:
                filename = os.path.basename(image_path)
                
                try:
                    with open(image_path, 'rb') as image_file:
                        if s3_service.upload_product_image(product_id, image_file, filename):
                            successful_uploads += 1
                            self.stdout.write(f'✓ Uploaded: {filename}')
                        else:
                            failed_uploads += 1
                            self.stdout.write(f'✗ Failed: {filename}')
                except Exception as e:
                    failed_uploads += 1
                    self.stdout.write(f'✗ Error with {filename}: {str(e)}')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Upload complete! Success: {successful_uploads}, Failed: {failed_uploads}'
                )
            )

        else:
            self.stdout.write(
                self.style.ERROR(
                    'Please provide both --product-id and --image-dir, or use --clear-cache'
                )
            )
