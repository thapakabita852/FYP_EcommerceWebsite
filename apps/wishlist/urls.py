from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('view/', views.view_wishlist, name='view_wishlist'),
    path('count/', views.get_wishlist_count, name='get_wishlist_count'),
]