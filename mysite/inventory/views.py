from django.shortcuts import render
from django.http import HttpResponse
import os
from models import Item


def item_list(request):
    item_list = Item.objects.order_by()
    context_dict = {'items': item_list}
    return render(request, 'inventory/item_list.html', context=context_dict)