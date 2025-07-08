from rest_framework import serializers
from .models import AmigurumiProduct

class AmigurumiProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = AmigurumiProduct
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'image_s3_path', 'is_featured', 'is_available', 'created_at']
    
    def get_image(self, obj):
        """Return the full S3 URL for the image"""
        return obj.image_url
