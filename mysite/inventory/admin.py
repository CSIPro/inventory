from django.contrib import admin
from .models import *
import datetime
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Owner)
admin.site.register(Item)
admin.site.register(IndividualItem)
admin.site.register(ItemImages)


# Action to return item in admin and add return date.
def return_item(modeladmin, request, queryset):
    for borrowed_item in queryset:

        borrowed_item.is_returned = True
        borrowed_item.date_returned = datetime.date.today()

        # Individual item (id=1, etc)
        individual_item = borrowed_item.item
        individual_item.is_borrowed = False
        individual_item.save()

        # General Item (RasPi, HDMi, etc)
        # Increase available total items by 1 and subtract the currently borrowed count by 1.
        general_item = individual_item.item
        general_item.available_count += 1
        general_item.current_borrowed -= 1
        general_item.save()

        borrowed_item.save()


# Item was borrowed by error or unintentionally
def soft_return(modeladmin, request, queryset):
    for borrowed_item in queryset:

        # Individual item (id=1, etc)
        individual_item = borrowed_item.item
        individual_item.is_borrowed = False
        individual_item.save()

        # General Item (RasPi, HDMi, etc)
        # Since this is soft_return, difference with normal return_item is that
        # times_borrowed will be decremented since it was borrowed by accident/error
        general_item = individual_item.item

        general_item.times_borrowed -= 1

        general_item.available_count += 1
        general_item.current_borrowed -= 1
        general_item.save()

        # ItemBorrowed record/object is deleted
        borrowed_item.delete()


class ItemBorrowedAdmin(admin.ModelAdmin):
    #  Items that get displayed in admin panel (table)
    list_display = ['item', 'user', 'date_borrowed', 'is_returned']
    actions = [return_item, soft_return]

admin.site.register(ItemBorrowed, ItemBorrowedAdmin)


# ------------------------------------------------------------------------
# Making UserProfile available to be edited/updated directly in User Admin.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
