from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'sales_count')
    list_filter = ('category',)  # Enable filtering by category

admin.site.register(Product, ProductAdmin)
