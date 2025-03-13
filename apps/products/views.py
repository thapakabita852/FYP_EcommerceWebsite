from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator

def landing_page(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ✅ Select products that are **manually** marked as trending
    trending_products = Product.objects.filter(is_trending=True).order_by('-created_at')[:6]

    # Optional: If no trending products exist, return None (or handle differently)
    if not trending_products.exists():
        trending_products = None  # Or remove this line if you want an empty section

    context = {
        'trending_products': trending_products,
        'page_obj': page_obj,
    }
    return render(request, 'landing.html', context)

def accessories_view(request):
    products = Product.objects.filter(category='accessories')  # Example query
    return render(request, 'products/accessories.html', {'products': products})

def eco_friendly_view(request):
    products = Product.objects.filter(category='eco_friendly')  # Example query
    return render(request, 'products/eco_friendly.html', {'products': products})


def clothing_view(request):
    # Initial query to get all clothing products
    products = Product.objects.filter(category="clothing")  # Base QuerySet

    # Get filter values from the GET request
    sort_by = request.GET.get('sort_by')
    category = request.GET.get('category')
    size = request.GET.getlist('size')  # Checkbox returns list
    sale_new = request.GET.get('sale_new')
    style = request.GET.get('style')
    color = request.GET.get('color')
    body_fit = request.GET.get('body_fit')

    # Apply filters based on selected options
    if category:
        products = products.filter(category=category)
    if size:
        products = products.filter(size__in=size)
    if sale_new:
        products = products.filter(sale_new=sale_new)
    if style:
        products = products.filter(style=style)
    if color:
        products = products.filter(color=color)
    if body_fit:
        products = products.filter(body_fit=body_fit)

    # Sorting products based on selected options
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # Render the filtered products to the template
    return render(request, 'products/clothing.html', {'products': products})


