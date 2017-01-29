from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

# 3rd party
from sorl.thumbnail import ImageField


# CSI, Unison, Erick, etc.
class Owner(models.Model):

    owner_name = models.CharField(max_length=45)

    def __str__(self):
        return self.owner_name


# Item table
class Item(models.Model):

    # Columns
    item_name = models.CharField(max_length=85)
    item_description = models.CharField(max_length=250)
    available_count = models.PositiveIntegerField()
    current_borrowed = models.PositiveIntegerField()
    item_owner = models.ForeignKey(Owner)

    def __str__(self):
        return '{} - Disponibles:{}'.format(self.item_name, self.available_count)


def item_directory_path(instance, filename):
        # for imges be uploaded to MEDIA_ROOT/item_<id>/<filename>
        return 'item_{0}/{1}'.format(instance.item.id, filename)


# Cada item va a tener un set de multiples imagenes.
class ItemImages(models.Model):

    item = models.ForeignKey(Item)
    img = models.ImageField(upload_to=item_directory_path)  # uploads to MEDIA/item_id/<img_path>

    def __str__(self):
        return self.img.url


class ItemBorrowed(models.Model):

    item = models.ForeignKey(Item)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_borrowed = models.DateField(auto_now=True)

    def __str__(self):
        return '{} se llevo un/a {}'.format(self.user, self.item.item_name)