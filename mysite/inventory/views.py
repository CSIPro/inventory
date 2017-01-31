from django.http import Http404
from django.shortcuts import render
from .models import Item


# For /inventory/
def index(request):
    item_list = Item.objects.all()
    context_dict = {'items': item_list}

    return render(request, 'inventory/item_list.html', context=context_dict)


# pk = item_id
def detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        raise Http404('Item no existe.')  # TODO: Planning on redirecting to custom 404 page in future

    context = {
        'item': item,
    }

    return render(request, 'inventory/item_detail.html', context)
