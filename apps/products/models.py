from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('eco-friendly', 'Eco-Friendly'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sales_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='clothing')

    def __str__(self):
        return self.title
