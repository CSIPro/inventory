from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Item, ItemBorrowed, UserProfile
from django.db.models import Q
import csv


# Function for re-using of pagination feature in different views.
def paginate(page, paginator, queryset):
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    return queryset


# For /inventory/
def index(request):
    items = Item.objects.all()
    paginator = Paginator(items, 12)

    page = request.GET.get('page')
    items = paginate(page, paginator, items)

    context = {'items': items}

    return render(request, 'inventory/item_list.html', context)


# Search item
def item_search(request):
    items = Item.objects.all()

    # For search form
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(
            Q(item_name__icontains=query)
        ).distinct()

    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    items = paginate(page, paginator, items)

    context = {'items': items, 'query': query}

    return render(request, 'inventory/item_list.html', context)


# pk = item_id
def detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        raise Http404('Item doesn\'t exist.')

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
        raise Http404('Item doesn\'t exist.')

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


# Export feature for user profile (exports user's registers to csv)
def csv_export(request, username):
    user = User.objects.filter(username=username)
    registers = ItemBorrowed.objects.filter(user=user)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(username)

    writer = csv.writer(response)
    # CSV Header
    writer.writerow([
        'Item',
        'Date Borrowed',
        'Is Returned?',
        'Date Returned'
    ])
    # Rows
    for obj in registers:
        writer.writerow([
            obj.item.item.item_name,
            obj.date_borrowed,
            obj.is_returned,
            obj.date_returned,
        ])

    return response
