from django.contrib import admin
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ('added_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'items_count')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    inlines = [WishlistItemInline]

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = 'Items Count'


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'wishlist', 'added_at')
    list_filter = ('added_at', 'wishlist__user')
    search_fields = ('product__title', 'wishlist__user__username')