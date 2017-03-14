from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item, IndividualItem, UserProfile


# Creates a new IndividualItem object whenever an Item object is created.
@receiver(post_save, sender=Item)
def create_individual_item(sender, instance, created, **kwargs):
    if created:
        # Gets the total available items.
        total = instance.available_count

        # Creates a new IndividualItem object for total items available.
        for item in range(total):
            IndividualItem.objects.create(item=instance)


# -----------------------------------------------------------------------
# User shit that can be moved to another app.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
