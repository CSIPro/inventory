from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Item, ItemBorrowed


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


# pk = item_id
def borrow(request, pk):
    try:
        item = Item.objects.get(pk=request.POST['item'])
    except Item.DoesNotExist:
        raise Http404('Item no existe.')  # TODO: Planning on redirecting to custom 404 page in future

    else:
        # Gets the first item that's not borrowed yet.
        unborrowed_individual_item = item.individualitem_set.filter(is_borrowed=False)[0]

        # Change the unborrowerd to borrowed = True
        unborrowed_individual_item.is_borrowed = True
        unborrowed_individual_item.save()

        # Creating new ItemBorrowed object
        borrowed = ItemBorrowed(item=item, user=request.user)
        borrowed.save()

        # Changing item's attributes
        item.available_count -= 1
        item.current_borrowed += 1

        item.save()

        # TODO: validate if there are still items left to be borrowed or not.

        return render(request, 'inventory/admin.html', {'item': item})
