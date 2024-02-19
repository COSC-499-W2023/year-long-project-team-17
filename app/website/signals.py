from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    #Creates a profile for when a new user is added
    if created:
        Profile.objects.create(user=instance)

