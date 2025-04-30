from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'date',]
    inlines = [OrderItemInline]
    list_filter = ['status']  # Allow filtering by status
    list_editable = ['status'] # Allow to edit the status


admin.site.register(Order, OrderAdmin)


