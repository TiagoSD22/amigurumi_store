from django.contrib import admin
from .models import AmigurumiProduct

@admin.register(AmigurumiProduct)
class AmigurumiProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_featured', 'is_available', 'created_at']
    list_filter = ['category', 'is_featured', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_available']
