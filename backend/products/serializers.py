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
        # Check if force_refresh parameter was passed in the request
        request = self.context.get('request')
        force_refresh = False
        
        if request and request.query_params:
            force_refresh = request.query_params.get('force_refresh', '').lower() in ['true', '1', 'yes']
        
        return obj.get_images(force_refresh=force_refresh)
    
    def get_primary_image(self, obj):
        """Return the primary image for the product"""
        # Check if force_refresh parameter was passed in the request
        request = self.context.get('request')
        force_refresh = False
        
        if request and request.query_params:
            force_refresh = request.query_params.get('force_refresh', '').lower() in ['true', '1', 'yes']
        
        return obj.get_primary_image(force_refresh=force_refresh)
