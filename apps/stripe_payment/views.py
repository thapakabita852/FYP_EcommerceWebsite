from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import stripe
from django.http import HttpResponse
from apps.products.models import Product
from apps.orders.models import Order, OrderItem
from apps.cart.models import Cart, CartItem
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY

# Define your domain for success and cancel URLs
YOUR_DOMAIN = settings.YOUR_DOMAIN if hasattr(settings,
                                              'YOUR_DOMAIN') else 'http://127.0.0.1:8000'  # Replace with your actual domain in settings.py


def create_checkout_session(request):
    if request.method == 'POST':
        # Debug: Print the entire POST data
        print("Request POST data:", request.POST)

        line_items = []
        # Assuming product data is sent as a list of dicts: [{'product_id': 1, 'quantity': 2}, ...]
        # product_data = request.POST.getlist('product_data') # Or however you send the data

        # Assuming product IDs and quantities are sent as separate lists in POST
        total_amount_str = request.POST.get('total_amount')

        # Debug: Print total_amount received
        print("Received total_amount:", total_amount_str)

        # Debug: Print total_amount value and type
        print(f"Total amount value: {total_amount_str}, Type: {type(total_amount_str)}")

        try:
            total_amount = float(total_amount_str)
            # Stripe requires amount in cents
            total_amount_cents = int(total_amount * 100)
        except (ValueError, TypeError):
            return HttpResponse("Invalid total amount.", status=400)

        # Create a single line item for the total amount
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Order Total',  # Generic name for the total amount
                },
                'unit_amount': total_amount_cents,  # Amount in cents
            },
            'quantity': 1,  # Quantity is 1 for the total amount
        })

        if total_amount_cents <= 0:
            return HttpResponse("Invalid total amount.", status=400)

        # Check if line_items is empty after processing
        if not line_items:
            return HttpResponse("Your cart is empty or contains invalid items.", status=400)

        try:
            # Debug: Print line_items before creating session
            print("Line items for Stripe:", line_items)

            # Debug: Print before Stripe session creation
            print("Attempting to create Stripe checkout session...")

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                client_reference_id=request.user.id,
                mode='payment',
                success_url=YOUR_DOMAIN + '/stripe/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )

            # Debug: Print after successful Stripe session creation
            print("Stripe checkout session created successfully.")
            # Debug: Print the checkout session URL
            print("Checkout session URL:", checkout_session.url)
            # Debug: Print before redirect
            print("Debug: Print before redirect")
            return redirect(checkout_session.url)


        except stripe.error.StripeError as e:
            print("Stripe checkout session created successfully.")
            # Debug: Print the checkout session URL
            print("Checkout session URL:", checkout_session.url)
            return redirect(checkout_session.url)


def success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect(reverse('accounts:dashboard'))  # Or an error page

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        user_id = session.client_reference_id
        user = get_object_or_404(User, id=user_id)

        # Create Order
        order = Order.objects.create(
            user=user,
            total_price=session.amount_total / 100,  # Amount in dollars
            status='Paid'
        )

        # Create Order Items from Cart Items
        cart = get_object_or_404(Cart, user=user)
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.total_price
            )

        # Clear the cart
        cart.items.all().delete()

        return render(request,'stripe_payment/success.html')

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return HttpResponse(f"Stripe Error: {e}", status=400)
    except Exception as e:
        # Handle other errors
        return HttpResponse(f"An error occurred: {e}", status=500)


from django.contrib.auth.models import User  # Import User model


def cancel(request):
    # Redirect to the dashboard page if the payment is cancelled
    return redirect(reverse('accounts:dashboard'))