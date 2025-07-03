from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.AmigurumiProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.AmigurumiProductDetailView.as_view(), name='product-detail'),
    path('products/featured/', views.featured_products, name='featured-products'),
    path('products/category/<str:category>/', views.products_by_category, name='products-by-category'),
]
