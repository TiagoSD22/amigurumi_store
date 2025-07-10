from django.db import models

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
    image_s3_path = models.CharField(max_length=500, help_text="S3 path to the product image")
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        """Generate full S3 URL for the product image"""
        from django.conf import settings
        bucket_name = getattr(settings, 'AWS_S3_BUCKET_NAME', 'product-image-collection')
        s3_base_url = getattr(settings, 'AWS_S3_BASE_URL', 'http://localhost.localstack.cloud:4566')
        return f"{s3_base_url}/{bucket_name}/{self.id}/{self.image_s3_path}"
