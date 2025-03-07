from django.shortcuts import render
from .models import Product

def landing_page(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    return render(request, 'landing.html', {'products': products})

def landing_page(request):
    # Handle category filtering for products list
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Fetch trending products (using sales_count filter)
    trending_products = Product.objects.filter(sales_count__gt=0).order_by('-sales_count')[:6]
    # Fallback: if no product qualifies, fetch the latest products
    if not trending_products.exists():
        trending_products = Product.objects.all().order_by('-id')[:6]

    if request.user.is_authenticated:
        try:
            cart = request.user.cart
            cart_count = cart.items.count()
        except AttributeError:
            cart_count = 0
        profile = request.user.profile
        context = {
            'trending_products': trending_products,
            'cart_count': cart_count,
            'profile': profile,
            'user': request.user,
            'products': products,
        }
        # Logged-in users see the dashboard template
        return render(request, 'accounts/dashboard.html', context)
    else:
        context = {
            'trending_products': trending_products,
            'cart_count': 0,
            'products': products,
        }
        # Non–logged-in users see the landing template
        return render(request, 'landing.html', context)


def clothing_view(request):
    return render(request, 'products/clothing.html')

def accessories_view(request):
    return render(request, 'products/accessories.html')

def eco_friendly_view(request):
    return render(request, 'products/eco_friendly.html')