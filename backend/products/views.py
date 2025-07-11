from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import AmigurumiProduct
from .serializers import AmigurumiProductSerializer

class AmigurumiProductListView(generics.ListAPIView):
    """List all amigurumi products"""
    queryset = AmigurumiProduct.objects.filter(is_available=True)
    serializer_class = AmigurumiProductSerializer
    
    def get_serializer_context(self):
        """Pass request context to serializer for force_refresh support"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class AmigurumiProductDetailView(generics.RetrieveAPIView):
    """Get a single amigurumi product"""
    queryset = AmigurumiProduct.objects.filter(is_available=True)
    serializer_class = AmigurumiProductSerializer
    
    def get_serializer_context(self):
        """Pass request context to serializer for force_refresh support"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['GET'])
def featured_products(request):
    """Get featured amigurumi products"""
    products = AmigurumiProduct.objects.filter(is_featured=True, is_available=True)
    serializer = AmigurumiProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def products_by_category(request, category):
    """Get products by category"""
    products = AmigurumiProduct.objects.filter(category=category.upper(), is_available=True)
    serializer = AmigurumiProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)
