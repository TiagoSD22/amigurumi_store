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
    image = models.ImageField(upload_to='amigurumi/')
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
