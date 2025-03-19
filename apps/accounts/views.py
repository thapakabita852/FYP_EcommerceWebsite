import re
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
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
    if re.search(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|123|234|345|456|567|678|789|890)', password, re.IGNORECASE):
        return "Password must not contain sequential characters."
    return None

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

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

        user = User.objects.create_user(username=name, password=password)

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('accounts:login')

    return redirect('accounts:login_signup')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Set a minimum password length
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



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

def password_reset_view(request):
    """Display the password reset form"""
    return render(request, 'accounts/password_reset.html', {'username_verified': False})


def password_reset_confirm(request):
    """Process the password reset request"""
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if we're in the verification step or password reset step
        if 'new_password' in request.POST:
            # We're in the password reset step
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            try:
                user = User.objects.get(username=username)

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Your password has been successfully reset. You can now log in.")
                    return redirect('accounts:login')
                else:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'accounts/password_reset.html', {
                        'username_verified': True,
                        'username': username
                    })
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect('accounts:password_reset')
        else:
            # We're in the username verification step
            try:
                user = User.objects.get(username=username)
                # Username exists, show the password reset form
                return render(request, 'accounts/password_reset.html', {
                    'username_verified': True,
                    'username': username
                })
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect('accounts:password_reset')

    return redirect('accounts:password_reset')