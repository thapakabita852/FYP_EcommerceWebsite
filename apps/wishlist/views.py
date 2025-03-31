from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.products.models import Product
from .models import Wishlist, WishlistItem
from django.shortcuts import render


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    # Check if product is already in wishlist
    if not WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        return JsonResponse({'status': 'added', 'wishlist_count': wishlist.items.count()})
    return JsonResponse({'status': 'exists', 'wishlist_count': wishlist.items.count()})


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    WishlistItem.objects.filter(wishlist=wishlist, product=product).delete()
    return JsonResponse({'status': 'removed', 'wishlist_count': wishlist.items.count()})


@login_required
def view_wishlist(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})


@login_required
def get_wishlist_count(request):
    wishlist_count = 0
    wishlist = Wishlist.objects.filter(user=request.user).first()
    if wishlist:
        wishlist_count = wishlist.items.count()
    return JsonResponse({'wishlist_count': wishlist_count})