from django.shortcuts import render
from .models import Item


# For /inventory/
def index(request):
    item_list = Item.objects.all()
    context_dict = {'items': item_list}

    return render(request, 'inventory/item_list.html', context=context_dict)