# S3 Image Service Documentation

## Overview

This implementation refactors the AmigurumiProduct model to use a service-based approach for handling product images stored in S3. Images are no longer stored in the database; instead, they are dynamically retrieved from S3 with caching for optimal performance.

## Key Components

### 1. S3ImageService (`products/services.py`)

A comprehensive service class that handles:
- **Image retrieval** from S3 with presigned URLs
- **Caching** of presigned URLs to avoid repeated S3 calls
- **Cache invalidation** when URLs expire
- **Image upload** and deletion operations
- **Environment-aware** S3 client configuration

### 2. Updated AmigurumiProduct Model (`products/models.py`)

The model has been refactored to:
- Remove the `image_s3_path` field
- Add a lazy `images` property that returns all product images
- Add a `primary_image` property for the first image
- Include cache invalidation methods

### 3. Updated Serializer (`products/serializers.py`)

The serializer now returns:
- `images`: List of all product images with presigned URLs
- `primary_image`: The first image for backward compatibility

## Usage

### Basic Usage

```python
from products.models import AmigurumiProduct

# Get a product
product = AmigurumiProduct.objects.get(id=1)

# Get all images (lazy loaded and cached)
images = product.images
# Returns: [{'url': 'presigned_url', 'filename': 'image1.jpg', 'key': '1/image1.jpg', 'expires_at': datetime}, ...]

# Get primary image
primary = product.primary_image
# Returns: {'url': 'presigned_url', 'filename': 'image1.jpg', 'key': '1/image1.jpg', 'expires_at': datetime}
```

### Using the Service Directly

```python
from products.services import S3ImageService

service = S3ImageService()

# Get images for a product
images = service.get_product_images(product_id=1)

# Upload an image
with open('image.jpg', 'rb') as f:
    service.upload_product_image(product_id=1, image_file=f, filename='image.jpg')

# Delete an image
service.delete_product_image(product_id=1, filename='image.jpg')

# Invalidate cache
service.invalidate_product_cache(product_id=1)
```

### Command Line Upload Script

Use the enhanced upload script:

```bash
# Basic usage (local environment)
python upload_product_images_to_s3.py --product_id=1 --images="./sample1.png ./sample2.png"

# Specify environment
python upload_product_images_to_s3.py --stack="local" --product_id=1 --images="./sample1.png ./sample2.png"

# Use Django service (recommended)
python upload_product_images_to_s3.py --product_id=1 --images="./sample1.png ./sample2.png" --use-service
```

### Django Management Command

Upload images via Django management command:

```bash
# Upload images for a product
python manage.py upload_images --product-id=1 --image-dir="./product_images/"

# Clear cache for all products
python manage.py upload_images --clear-cache
```

## Configuration

### Settings

Add these settings to your Django settings:

```python
# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# S3 Image Service settings
S3_PRESIGNED_URL_CACHE_TIMEOUT = 3600  # 1 hour
S3_PRESIGNED_URL_EXPIRATION = 3600  # 1 hour

# AWS S3 settings
AWS_S3_BUCKET_NAME = 'product-image-collection'
AWS_S3_ENDPOINT_URL = 'http://localhost:4566'  # For LocalStack
```

### Environment Variables

For different environments:

- **Local**: Uses LocalStack endpoint
- **Demo/Stage/Prod**: Uses AWS S3 (configure credentials via AWS CLI or environment variables)

## S3 Structure

Images are stored in S3 with the following structure:
```
product-image-collection/
├── 1/
│   ├── image1.jpg
│   ├── image2.png
│   └── image3.gif
├── 2/
│   ├── front.jpg
│   └── back.jpg
```

## Caching Strategy

1. **First Request**: Fetches image list from S3, generates presigned URLs, caches for 1 hour
2. **Subsequent Requests**: Returns cached URLs if still valid
3. **Cache Expiration**: Automatically refreshes when URLs are close to expiring (5-minute buffer)
4. **Manual Invalidation**: Use `product.invalidate_image_cache()` or service methods

## Migration

The migration `0004_remove_image_s3_path_field.py` removes the old `image_s3_path` field. Make sure to run:

```bash
python manage.py migrate
```

## API Response Format

The API now returns:

```json
{
  "id": 1,
  "name": "Cute Bear",
  "description": "Adorable teddy bear",
  "price": "25.00",
  "category": "ANIMAL",
  "images": [
    {
      "url": "https://s3.amazonaws.com/bucket/1/image1.jpg?presigned_params",
      "filename": "image1.jpg",
      "key": "1/image1.jpg",
      "expires_at": "2025-07-10T15:30:00Z"
    }
  ],
  "primary_image": {
    "url": "https://s3.amazonaws.com/bucket/1/image1.jpg?presigned_params",
    "filename": "image1.jpg",
    "key": "1/image1.jpg",
    "expires_at": "2025-07-10T15:30:00Z"
  },
  "is_featured": true,
  "is_available": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

## Performance Considerations

- **Lazy Loading**: Images are only fetched when accessed
- **Caching**: Presigned URLs are cached to reduce S3 API calls
- **Batch Operations**: Use the service methods for bulk operations
- **Cache Invalidation**: Automatically handled when images are uploaded/deleted

## Error Handling

The service includes comprehensive error handling:
- S3 connection errors
- Missing bucket/objects
- Invalid credentials
- Cache errors

All errors are logged appropriately and don't break the application flow.
