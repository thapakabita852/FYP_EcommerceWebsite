from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    # New fields for body measurements:
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in centimeters
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in kilograms
    bust = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
