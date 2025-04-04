from django.db import models

class Product(models.Model):
    objects = None
    title = models.CharField(max_length=255, default="Untitled Product")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_trending = models.BooleanField(default=False)
    description = models.TextField(default="No description available.")
    category = models.CharField(
        max_length=50,
        choices=[
            ('clothing', 'Clothing'),
            ('accessories', 'Accessories'),
            ('eco_friendly', 'Eco-Friendly')
        ],
        default='clothing',
        db_index=True  # Adding index here
    )

    # Clothing Type (Only for Clothing & Eco-Friendly Apparel)
    clothing_type = models.CharField(
        max_length=50,
        choices=[
            ('casual', 'Casual'),
            ('formal', 'Formal'),
            ('sporty', 'Sporty'),
            ('party_wear', 'Party Wears'),
            ('jackets', 'Jackets')
        ],
        blank=True,
        null=True
    )

    # Size (Only for Clothing)
    size = models.CharField(
        max_length=5,
        choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')],
        blank=True,
        null=True,
        db_index=True  # Adding index here
    )

    # Sale/New Season
    sale_new = models.CharField(
        max_length=10,
        choices=[('sale', 'Sale'), ('new', 'New Season')],
        blank=True,
        null=True
    )

    # Style (For Clothing)
    style = models.CharField(
        max_length=50,
        choices=[
            ('casual', 'Casual'),
            ('formal', 'Formal'),
            ('sporty', 'Sporty'),
            ('party_wear', 'Party Wears')
        ],
        blank=True,
        null=True
    )

    subcategory = models.CharField(
        max_length=50,
        choices=[
            ('necklaces', 'Necklaces'),
            ('earrings', 'Earrings'),
            # other accessory types
        ],
        blank=True,
        null=True
    )

    necklace_type = models.CharField(
        max_length=50,
        choices=[
            ('choker', 'Chokers'),
            ('pendant', 'Pendants'),
            ('chain', 'Chains'),
        ],
        blank=True,
        null=True
    )

    # Earring Type (For Accessories)
    earring_type = models.CharField(
        max_length=50,
        choices=[
            ('stud', 'Stud'),
            ('hoop', 'Hoop'),
            ('drop', 'Drop')
        ],
        blank=True,
        null=True
    )

    # Color (For Accessories)
    accessory_color = models.CharField(max_length=7, blank=True, null=True)  # Renamed to avoid conflict

    # Color (For Clothing)
    color = models.CharField(max_length=7, blank=True, null=True, db_index=True)  # Adding index here

    # Body Fit (For Clothing)
    body_fit = models.CharField(
        max_length=20,
        choices=[('petite', 'Petite'), ('regular', 'Regular'), ('plus_size', 'Plus Size')],
        blank=True,
        null=True
    )

    # 🌱 Material (Only for Eco-Friendly Products)
    material = models.CharField(
    max_length=50,
    choices=[
        ('vegan_leather', 'Vegan Leather'),
        ('organic_cotton', 'Organic Cotton'),
        ('hemp', 'Hemp'),
        ('bamboo_cotton', 'Bamboo Cotton')
    ],
    blank=True,
    null=True
)

    # 🌱 Sustainability Level (Only for Eco-Friendly Products)
    sustainability_level = models.CharField(
        max_length=50,
        choices=[
            ('basic', 'Basic Eco-Friendly'),
            ('certified', 'Certified Sustainable'),
            ('premium', 'High-Grade Sustainable')
        ],
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    sales_count = models.IntegerField(default=0)

    class AboutUs(models.Model):
        title = models.CharField(max_length=255)
        description = models.TextField()
        team_image = models.ImageField(upload_to='about_us_images/', null=True, blank=True)

    def str(self):
        return self.title