from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'category', 'sales_count', 'is_trending', 'necklace_type', 'earring_type']  # Added necklace_type and earring_type
    search_fields = ['title', 'category', 'description', 'necklace_type', 'earring_type']  # Added necklace_type and earring_type to search
    list_filter = ['category', 'is_trending', 'sale_new', 'style', 'necklace_type', 'earring_type']  # Added necklace_type and earring_type to filters

admin.site.register(Product, ProductAdmin)
