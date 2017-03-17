from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Item, ItemBorrowed, UserProfile

from django.db.models import Q


# For /inventory/
def index(request):
    items = Item.objects.all()

    # For search form
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(item_name__icontains=query)
        ).distinct()

    context = {'items': items, 'query': query}

    return render(request, 'inventory/item_list.html', context)


# pk = item_id
def detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        raise Http404('Item no existe.')  # TODO: Planning on redirecting to custom 404 page in future

    images = item.itemimages_set.all()[1:]

    context = {
        'item': item,
        'images': images,
    }

    return render(request, 'inventory/item_detail.html', context)


# pk = item_id
@login_required
def borrow(request, pk):
    try:
        item = Item.objects.get(pk=request.POST['item'])
    except Item.DoesNotExist:
        raise Http404('Item no existe.')  # TODO: Planning on redirecting to custom 404 page in future

    else:

        all_unborrowed_items = item.individualitem_set.filter(is_borrowed=False)

        # Checks if there are any unborrowed items. If not, redirect to error page, for now. (Or can generate modal)
        if not all_unborrowed_items:
            return render(request, 'inventory/no_items.html', {'item': item})

        # Gets the first item that's not borrowed yet.
        unborrowed_individual_item = all_unborrowed_items[0]

        # Change the unborrowerd to borrowed = True
        unborrowed_individual_item.is_borrowed = True
        unborrowed_individual_item.save()

        # Creating new ItemBorrowed object
        borrowed = ItemBorrowed(item=unborrowed_individual_item, user=request.user)
        borrowed.save()

        # Changing item's attributes
        item.available_count -= 1
        item.current_borrowed += 1

        item.save()

        return render(request, 'inventory/admin.html', {'individual_item': unborrowed_individual_item})


# username = username gotten from user_items urlpattern
def user_items(request, username):
    user = User.objects.filter(username=username)
    profile = UserProfile.objects.get(user=user)

    borrowed_items = ItemBorrowed.objects.filter(user=user, is_returned=False)
    history = ItemBorrowed.objects.filter(user=user, is_returned=True)

    total = len(borrowed_items) + len(history)
    current_borrowed = len(borrowed_items)
    history_count = len(history)

    return render(request, 'inventory/user_items.html', {
        'borrowed_items': borrowed_items,
        'history': history,
        'username': username,
        'profile_pic': profile.pic,
        'total': total,
        'current': current_borrowed,
        'history_count': history_count,
    })
