from django.db import models
from django.utils.functional import cached_property

class AmigurumiProduct(models.Model):
    """Model for Amigurumi products"""
    
    CATEGORY_CHOICES = [
        ('ANIMAL', 'Animal'),
        ('DOLL', 'Doll'),
        ('CHARACTER', 'Character'),
        ('ACCESSORIES', 'Accessories'),
        ('SEASONAL', 'Seasonal'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ANIMAL')
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_images(self, force_refresh: bool = False):
        """
        Get all images for this product from S3 with presigned URLs
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data from S3
            
        Returns:
            List of dictionaries containing image data with presigned URLs
        """
        from .services import S3ImageService
        
        service = S3ImageService()
        return service.get_product_images(self.id, force_refresh=force_refresh)
    
    @cached_property
    def images(self):
        """
        Get all images for this product from S3 with presigned URLs
        This is a lazy property that will be cached per request
        """
        return self.get_images(force_refresh=False)
    
    def get_primary_image(self, force_refresh: bool = False):
        """
        Get the first image as the primary image
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data from S3
        """
        images = self.get_images(force_refresh=force_refresh)
        if images:
            return images[0]
        return None
    
    @property
    def primary_image(self):
        """Get the first image as the primary image"""
        return self.get_primary_image(force_refresh=False)
    
    def invalidate_image_cache(self):
        """Invalidate the cached images for this product"""
        from .services import S3ImageService
        
        service = S3ImageService()
        service.invalidate_product_cache(self.id)
        
        # Also clear the cached_property
        if hasattr(self, '_images'):
            delattr(self, '_images')
