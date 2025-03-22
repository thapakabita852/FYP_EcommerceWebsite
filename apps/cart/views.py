from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Cart, CartItem

from django.http import JsonResponse

from .. import products
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # Increase quantity if already in cart
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def update_cart(request, item_id):
    """
    Update the quantity for a given cart item.
    Expects a POST with a 'quantity' value.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
    except ValueError:
        pass  # Optionally add error handling
    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, item_id):
    """
    Remove a cart item.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:view_cart')

@login_required
def get_cart_count(request):
    cart_count = 0
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_count = cart.items.count()
    return JsonResponse({'cart_count': cart_count})

def clothing_view(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.count()
    # Fetch products and other context data
    context = {
        'cart_count': cart_count,
        'products': products,  # Add your products here
    }
    return render(request, 'products:clothing.html', context)

@login_required
def accessories_view(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.count()
    # Fetch products and other context data
    context = {
        'cart_count': cart_count,
        'products': products,  # Add your products here
    }
    return render(request, 'products/accessories.html', context)

@login_required
def eco_friendly_view(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.count()
    # Fetch eco-friendly products
    products = Product.objects.filter(category='eco_friendly')
    context = {
        'cart_count': cart_count,
        'products': products,
    }
    return render(request, 'products/eco_friendly.html', context)
