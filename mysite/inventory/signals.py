from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item, IndividualItem


# Creates a new IndividualItem object whenever an Item object is created.
@receiver(post_save, sender=Item)
def create_individual_item(sender, instance, created, **kwargs):
    if created:
        # Gets the total available items.
        total = instance.available_count

        # Creates a new IndividualItem object for total items available.
        for item in range(total):
            IndividualItem.objects.create(item=instance)
