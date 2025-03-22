from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product
from decimal import Decimal

class Cart(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    @property
    def tax(self):
        tax_rate = Decimal('0.13')  # Explicitly create a Decimal
        return self.total_price * tax_rate

    @property
    def final_total(self):
        return self.total_price + self.tax

class CartItem(models.Model):
    objects = None
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
