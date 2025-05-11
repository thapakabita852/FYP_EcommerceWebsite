from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.orders.models import Order, OrderItem
from apps.cart.models import Cart, CartItem


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})


@login_required
def payment_page(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart:view_cart')

    total_price = sum(item.product.price * item.quantity for item in cart.items.all())
    # Render payment page with cart and total details (order not created yet)
    return render(request, 'orders/payment.html', {'total_price': total_price, 'cart': cart})


@login_required
def process_payment(request):
    if request.method == 'POST':
        # (Here, you could add real payment gateway processing)
        # For simulation, we assume payment is successful.

        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('cart:view_cart')

        # Create order from cart items
        order = Order.objects.create(user=request.user, status="Processing")
        total_price = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_price += item.product.price * item.quantity
        order.total_price = total_price
        order.save()

        # Clear the cart
        cart.items.all().delete()

        messages.success(request, "Payment processed successfully! Your order has been placed.")
        return redirect('orders:order_confirmation', order_id=order.id)
    else:
        return redirect('orders:payment')