import boto3
import logging
from django.conf import settings
from django.core.cache import cache
from datetime import datetime, timedelta
from typing import List, Optional
from botocore.exceptions import ClientError, NoCredentialsError
import os

logger = logging.getLogger(__name__)

class S3ImageService:
    """Service for handling S3 image operations with caching"""
    
    def __init__(self):
        self.bucket_name = getattr(settings, 'AWS_S3_BUCKET_NAME', 'product-image-collection')
        self.cache_timeout = getattr(settings, 'S3_PRESIGNED_URL_CACHE_TIMEOUT', 3600)  # 1 hour
        self.presigned_url_expiration = getattr(settings, 'S3_PRESIGNED_URL_EXPIRATION', 3600)  # 1 hour
        self.default_image_key = getattr(settings, 'S3_DEFAULT_IMAGE_KEY', 'image_not_found.png')
        self.s3_client = self._get_s3_client()
    
    def _get_s3_client(self):
        """Get S3 client based on environment settings"""
        try:
            if hasattr(settings, 'AWS_S3_ENDPOINT_URL') and settings.AWS_S3_ENDPOINT_URL:
                # LocalStack or custom endpoint
                return boto3.client(
                    's3',
                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                    aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', 'test'),
                    aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', 'test'),
                    region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1'),
                    use_ssl=getattr(settings, 'AWS_S3_USE_SSL', False),
                    verify=getattr(settings, 'AWS_S3_VERIFY', False)
                )
            else:
                # AWS production environment
                return boto3.client(
                    's3',
                    region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1')
                )
        except Exception as e:
            logger.error(f"Failed to create S3 client: {e}")
            raise
    
    def _get_cache_key(self, product_id: int) -> str:
        """Generate cache key for product images"""
        return f"product_images_{product_id}"
    
    def _list_product_images(self, product_id: int) -> List[str]:
        """List all images for a product from S3"""
        try:
            prefix = f"{product_id}/"
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                return []
            
            # Extract the image keys and filter out directories
            image_keys = []
            for obj in response['Contents']:
                key = obj['Key']
                # Skip if it's just the directory (ends with /)
                if not key.endswith('/'):
                    image_keys.append(key)
            
            return image_keys
        except ClientError as e:
            logger.error(f"Error listing images for product {product_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error listing images for product {product_id}: {e}")
            return []
    
    def _generate_presigned_urls(self, image_keys: List[str]) -> List[dict]:
        """Generate presigned URLs for a list of image keys"""
        presigned_urls = []
        
        for key in image_keys:
            try:
                presigned_url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': key},
                    ExpiresIn=self.presigned_url_expiration
                )
                
                # Extract filename from key
                filename = key.split('/')[-1]
                
                presigned_urls.append({
                    'url': presigned_url,
                    'filename': filename,
                    'key': key,
                    'expires_at': datetime.now() + timedelta(seconds=self.presigned_url_expiration),
                    'is_default': False
                })
            except ClientError as e:
                logger.error(f"Error generating presigned URL for {key}: {e}")
                continue
        
        return presigned_urls
    
    def _is_cache_valid(self, cached_data: dict) -> bool:
        """Check if cached presigned URLs are still valid"""
        if not cached_data or 'images' not in cached_data:
            return False
        
        # Check if any URL has expired (with 5 minute buffer)
        buffer_time = timedelta(minutes=5)
        current_time = datetime.now()
        
        for image_data in cached_data['images']:
            if 'expires_at' in image_data:
                expires_at = image_data['expires_at']
                if isinstance(expires_at, str):
                    expires_at = datetime.fromisoformat(expires_at)
                
                if current_time + buffer_time >= expires_at:
                    return False
        
        return True
    
    def get_product_images(self, product_id: int, force_refresh: bool = False) -> List[dict]:
        """
        Get product images with caching. If no images exist, return default image.
        
        Args:
            product_id: The ID of the product
            force_refresh: If True, bypass cache and fetch fresh data from S3
            
        Returns:
            List of dictionaries containing image data with presigned URLs
        """
        cache_key = self._get_cache_key(product_id)
        
        # Skip cache if force_refresh is True
        if not force_refresh:
            # Try to get from cache first
            cached_data = cache.get(cache_key)
            
            if cached_data and self._is_cache_valid(cached_data):
                logger.debug(f"Returning cached images for product {product_id}")
                return cached_data['images']
        else:
            logger.debug(f"Force refresh requested for product {product_id}, bypassing cache")
        
        # Cache miss, expired, or force refresh - fetch from S3
        logger.debug(f"Fetching images from S3 for product {product_id}")
        
        try:
            # List all images for this product
            image_keys = self._list_product_images(product_id)
            
            if not image_keys:
                # No images found for this product - use default image
                logger.debug(f"No images found for product {product_id}, using default image")
                default_image = self._get_default_image()
                default_images = [default_image]
                
                # Cache the default image result for shorter time
                cache_data = {
                    'images': default_images,
                    'cached_at': datetime.now(),
                    'is_default': True
                }
                
                cache.set(cache_key, cache_data, timeout=300)  # 5 minutes for default image
                return default_images
            
            # Generate presigned URLs for actual product images
            presigned_urls = self._generate_presigned_urls(image_keys)
            
            # Cache the results
            cache_data = {
                'images': presigned_urls,
                'cached_at': datetime.now(),
                'is_default': False
            }
            
            cache.set(cache_key, cache_data, timeout=self.cache_timeout)
            
            return presigned_urls
            
        except Exception as e:
            logger.error(f"Error fetching images for product {product_id}: {e}")
            # Return default image as fallback on error
            try:
                default_image = self._get_default_image()
                return [default_image]
            except Exception as fallback_error:
                logger.error(f"Error getting default image as fallback: {fallback_error}")
                return []
    
    def invalidate_product_cache(self, product_id: int):
        """Invalidate cache for a specific product"""
        cache_key = self._get_cache_key(product_id)
        cache.delete(cache_key)
        logger.info(f"Cache invalidated for product {product_id}")
    
    def upload_product_image(self, product_id: int, image_file, filename: str) -> bool:
        """
        Upload an image for a product to S3
        
        Args:
            product_id: The ID of the product
            image_file: The image file object
            filename: The filename to use in S3
            
        Returns:
            True if successful, False otherwise
        """
        try:
            s3_key = f"{product_id}/{filename}"
            
            self.s3_client.upload_fileobj(
                image_file,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ACL': 'public-read'}
            )
            
            # Invalidate cache for this product
            self.invalidate_product_cache(product_id)
            
            logger.info(f"Successfully uploaded {filename} for product {product_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading image {filename} for product {product_id}: {e}")
            return False
    
    def delete_product_image(self, product_id: int, filename: str) -> bool:
        """
        Delete an image for a product from S3
        
        Args:
            product_id: The ID of the product
            filename: The filename to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            s3_key = f"{product_id}/{filename}"
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            # Invalidate cache for this product
            self.invalidate_product_cache(product_id)
            
            logger.info(f"Successfully deleted {filename} for product {product_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting image {filename} for product {product_id}: {e}")
            return False
    
    def _get_default_image(self) -> dict:
        """
        Generate presigned URL for the default image
        
        Returns:
            Dictionary containing default image data with presigned URL
        """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': self.default_image_key},
                ExpiresIn=self.presigned_url_expiration
            )
            
            return {
                'url': presigned_url,
                'filename': self.default_image_key,
                'key': self.default_image_key,
                'expires_at': datetime.now() + timedelta(seconds=self.presigned_url_expiration),
                'is_default': True
            }
        except ClientError as e:
            logger.error(f"Error generating presigned URL for default image {self.default_image_key}: {e}")
            # Return a fallback structure if default image is not available
            return {
                'url': None,
                'filename': self.default_image_key,
                'key': self.default_image_key,
                'expires_at': datetime.now() + timedelta(seconds=self.presigned_url_expiration),
                'is_default': True,
                'error': 'Default image not found'
            }
        except Exception as e:
            logger.error(f"Unexpected error generating default image URL: {e}")
            return {
                'url': None,
                'filename': self.default_image_key,
                'key': self.default_image_key,
                'expires_at': datetime.now() + timedelta(seconds=self.presigned_url_expiration),
                'is_default': True,
                'error': str(e)
            }
