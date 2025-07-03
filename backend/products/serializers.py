from rest_framework import serializers
from .models import AmigurumiProduct

class AmigurumiProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmigurumiProduct
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'is_featured', 'is_available', 'created_at']
