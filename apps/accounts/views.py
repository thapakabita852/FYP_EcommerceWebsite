from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile  # Make sure to import Profile
from apps.orders.models import Order  # import the Order model
from apps.products.models import Product


def auth_view(request):
    return render(request, 'accounts/login_signup.html')


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'accounts:dashboard'))
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return redirect('accounts:auth')


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:auth')
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:auth')
        user = User.objects.create_user(username=name, password=password)
        login(request, user)
        return redirect('accounts:dashboard')
    return redirect('accounts:auth')


def logout_view(request):
    logout(request)
    return redirect('accounts:auth')


@login_required
def dashboard_view(request):
    trending_products = Product.objects.filter(sales_count__gt=0).order_by('-sales_count')[:6]
    try:
        cart = request.user.cart
        cart_count = cart.items.count()
    except AttributeError:
        cart_count = 0
    profile = request.user.profile
    return render(request, 'accounts/dashboard.html', {
        'trending_products': trending_products,
        'cart_count': cart_count,
        'profile': profile,
        'user': request.user,
    })



@login_required
def profile_view(request):
    # Retrieve or create the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.address = request.POST.get('address')
        profile.age = request.POST.get('age')
        profile.phone = request.POST.get('phone')
        profile.sex = request.POST.get('sex')
        profile.height = request.POST.get('height') or None
        profile.weight = request.POST.get('weight') or None
        profile.bust = request.POST.get('bust') or None
        profile.waist = request.POST.get('waist') or None
        profile.hips = request.POST.get('hips') or None
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('accounts:profile')
    return redirect('accounts:profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
            return redirect('accounts:change_password')

        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('accounts:change_password')

        request.user.set_password(new_password1)
        request.user.save()
        messages.success(request, "Password changed successfully. Please log in again.")
        return redirect('accounts:login')

    return render(request, 'accounts/change_password.html')


@login_required
def profile_view(request):
    # Get or create the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Fetch orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'accounts/profile.html', {'profile': profile, 'orders': orders})