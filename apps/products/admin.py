from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'category', 'sales_count', 'is_trending']  # Use 'title' instead of 'name'
    search_fields = ['title', 'category', 'description']  # Adjust search fields if necessary
    list_filter = ['category', 'is_trending', 'sale_new', 'style']  # Example of filters

admin.site.register(Product, ProductAdmin)
