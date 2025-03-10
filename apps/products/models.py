from django.db import models

class Product(models.Model):
    objects = None
    title = models.CharField(max_length=255, default="Untitled Product")  # Default title
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default price
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_trending = models.BooleanField(default=False)
    description = models.TextField(default="No description available.")  # Default description
    category = models.CharField(
        max_length=50,
        choices=[('clothing', 'Clothing'), ('accessories', 'Accessories'), ('eco_friendly', 'Eco-Friendly')],
        default='clothing'  # Default category
    )
    clothing_type = models.CharField(
        max_length=50,
        choices=[('casual', 'Casual'), ('formal', 'Formal'), ('sporty', 'Sporty'), ('boho', 'Boho'), ('jackets', 'Jackets')],
        blank=True,
        null=True
    )
    size = models.CharField(
        max_length=5,
        choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')],
        default='M'  # Default size
    )
    sale_new = models.CharField(
        max_length=10,
        choices=[('sale', 'Sale'), ('new', 'New Season')],
        blank=True,
        null=True,
        default=None  # Allowing null for optional field
    )
    style = models.CharField(
        max_length=50,
        choices=[('casual', 'Casual'), ('formal', 'Formal'), ('sporty', 'Sporty'), ('boho', 'Boho')],
        default='casual'  # Default style
    )
    color = models.CharField(max_length=7, blank=True, null=True, default=None)  # Allow blank and null
    body_fit = models.CharField(
        max_length=20,
        choices=[('petite', 'Petite'), ('regular', 'Regular'), ('plus_size', 'Plus Size')],
        blank=True,
        null=True,
        default=None  # Allow blank and null
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sales_count = models.IntegerField(default=0)  # Default to 0 for new products

    def __str__(self):
        return self.title  # Corrected method name

