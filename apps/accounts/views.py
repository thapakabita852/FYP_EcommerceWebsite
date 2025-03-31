
import re
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from apps.orders.models import Order
from apps.products.models import Product
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_str

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


def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.match(r'^[a-zA-Z]', password):
        return "Password must begin with a letter."
    if not any(char.isdigit() for char in password):
        return "Password must include at least one number."
    if not any(char.islower() for char in password):
        return "Password must include at least one lowercase letter."
    if not any(char.isupper() for char in password):
        return "Password must include at least one uppercase letter."
    if not any(char in '!";#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' for char in password):
        return "Password must include at least one symbol."
    if len(set(password)) < len(password):
        return "Password must not contain duplicate characters."
    if re.search(
            r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|123|234|345|456|567|678|789|890)',
            password, re.IGNORECASE):
        return "Password must not contain sequential characters."
    return None


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation checks
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:auth')

        validation_error = is_valid_password(password)
        if validation_error:
            messages.error(request, validation_error)
            return redirect('accounts:auth')

        try:
            password_validation.validate_password(password, user=None)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return redirect('accounts:auth')

        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:auth')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return redirect('accounts:auth')

        # Create user without email verification
        user = User.objects.create_user(
            username=name,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('accounts:login')

    return redirect('accounts:auth')


def verify_email(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        profile = user.profile
        profile.email_verified = True
        profile.save()
        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Invalid verification link.")
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
    profile, created = Profile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'orders': orders
    })


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


def logout_view(request):
    logout(request)
    return redirect('accounts:auth')
