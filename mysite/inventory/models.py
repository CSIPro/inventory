from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User


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
    current_borrowed = models.PositiveIntegerField(default=0)
    times_borrowed = models.PositiveIntegerField(default=0)
    item_owner = models.ForeignKey(Owner)

    # Less than 34% of items available to borrow.
    def few_left(self):
        total = self.available_count + self.current_borrowed
        avail = self.available_count
        return avail / total * 100 < 34

    # Between 34-67% of items available to borrow.
    def normal_left(self):
        total = self.available_count + self.current_borrowed
        avail = self.available_count
        return 34 <= avail / total * 100 < 67

    # More than 67% of items available to borrow.
    def many_left(self):
        total = self.available_count + self.current_borrowed
        avail = self.available_count
        return avail / total * 100 >= 67

    def none_left(self):
        return self.available_count == 0

    def __str__(self):
        return '{} - Disponibles:{}, Borrowed: {}'.format(self.item_name, self.available_count, self.current_borrowed)


# Each individual item (will have it's own ID and shit.)
class IndividualItem(models.Model):
    item = models.ForeignKey(Item)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return '{} ..... ID: {}..... Borrowed={}.'.format(self.item.item_name, self.pk, self.is_borrowed)


def item_directory_path(instance, filename):
        # for imges be uploaded to MEDIA_ROOT/item_<id>/<filename>
        return 'item_{0}/{1}'.format(instance.item.id, filename)


# Cada item va a tener un set de multiples imagenes.
class ItemImages(models.Model):

    item = models.ForeignKey(Item)
    img = models.ImageField(upload_to=item_directory_path)  # uploads to MEDIA/item_id/<img_path>

    def __str__(self):
        return self.item.item_name


# Relates to IndividualItem on a 1-1 relationship.
class ItemBorrowed(models.Model):

    item = models.ForeignKey(IndividualItem)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_borrowed = models.DateField(auto_now=True)

    # Date returned initializes to null so that we can change it once the item is returned.
    is_returned = models.BooleanField(default=False)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} se llevo un/a {} con id={}........ {} se ha devuelto.'\
            .format(self.user, self.item.item.item_name, self.item.id, 'SI' if self.is_returned else 'NO')


# User shit
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Temporary storage... thinking about moving this model to seperate app to
# keep all the relevant shit in it's group and modularity.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(null=True, blank=True, upload_to=user_directory_path)

    def __str__(self):
        return self.user.username


# For the IndividualItem creation.
from .signals import create_individual_item
# For User object creation => UserProfile
from .signals import create_user_profile, save_user_profile
