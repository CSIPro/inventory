from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Owner)
admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(ItemBorrowed)
