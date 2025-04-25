from django.db import models
from django.utils.timezone import now

class KhaltiTransaction(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    transaction_id = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()  # amount in paisa
    khalti_token = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
