from rest_framework import serializers
from .models import AmigurumiProduct

class AmigurumiProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = AmigurumiProduct
        fields = [
            'id', 'name', 'description', 'price', 'category', 
            'images', 'primary_image', 'is_featured', 'is_available', 
            'created_at', 'updated_at'
        ]
    
    def get_images(self, obj):
        """Return all images for the product with presigned URLs"""
        return obj.images
    
    def get_primary_image(self, obj):
        """Return the primary image for the product"""
        return obj.primary_image
