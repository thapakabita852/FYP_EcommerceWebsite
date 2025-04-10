from django.shortcuts import render
from django.core.paginator import Paginator
from apps.products.models import Product

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


def eco_friendly_view(request):
    products = Product.objects.filter(category="eco_friendly")  # Base QuerySet

    # Get filter values from the GET request
    sort_by = request.GET.get('sort_by')
    category = request.GET.get('category')
    clothing_type = request.GET.get('clothing_type')
    size = request.GET.getlist('size')  # Multiple selections
    sale_new = request.GET.get('sale_new')
    style = request.GET.get('style')
    color = request.GET.get('color')
    body_fit = request.GET.get('body_fit')

    # 🌱 New Filters for Eco-Friendly Products
    material = request.GET.get('material')
    sustainability_level = request.GET.get('sustainability_level')

    # Apply filters
    if category:
        products = products.filter(title__icontains=category)
    if clothing_type:
        products = products.filter(clothing_type=clothing_type)
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

    # 🌱 Apply Eco-Friendly Filters
    if material:
        products = products.filter(material=material)
    if sustainability_level:
        products = products.filter(sustainability_level=sustainability_level)

    # Sorting products
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

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

def accessories_view(request):
    products = Product.objects.filter(category='accessories')

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # Filter based on Subcategory (necklaces/earrings)
    subcategory = request.GET.get('subcategory')  # Changed from 'category' to 'subcategory'
    if subcategory:
        products = products.filter(subcategory=subcategory)

    # Filter based on Necklace Type
    necklace_type = request.GET.get('necklace_type')
    if subcategory == 'necklaces' and necklace_type:
        products = products.filter(necklace_type=necklace_type)

    # Filter based on Earring Type
    earring_type = request.GET.get('earring_type')
    if subcategory == 'earrings' and earring_type:
        products = products.filter(earring_type=earring_type)

    # Filter by Color
    color = request.GET.get('color')
    if color:
        products = products.filter(accessory_color=color)

    return render(request, 'products/accessories.html', {'products': products})

def about_us_view(request):
    return render(request, 'products/about_us.html')

def shop_now(request):
    category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')

    products = Product.objects.all()

    if category != 'all':
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/shop_now.html', {'products': page_obj})

