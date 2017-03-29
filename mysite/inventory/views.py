from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext

from .models import Item, ItemBorrowed, UserProfile
from .forms import UserForm, UserProfileForm
from django.db.models import Q
import csv
from django.core.mail import send_mail  # For email sending


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
    items = Item.objects.all().order_by('-times_borrowed')
    paginator = Paginator(items, 12)

    page = request.GET.get('page')
    items = paginate(page, paginator, items)

    context = {'items': items}

    return render(request, 'inventory/item_list.html', context)


# Search item
def item_search(request):
    items = Item.objects.all().order_by('-times_borrowed')

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

        # If there are no unborrowed items, the button to borrowe will be disabled (won't even go through to this view)

        # Gets the first item that's not borrowed yet.
        unborrowed_individual_item = all_unborrowed_items[0]

        # Change the unborrowerd to borrowed = True
        unborrowed_individual_item.is_borrowed = True
        unborrowed_individual_item.save()

        # Creating new ItemBorrowed object
        borrowed = ItemBorrowed(item=unborrowed_individual_item, user=request.user)
        borrowed.save()

        # Changing general item's attributes
        item.available_count -= 1
        item.current_borrowed += 1
        item.times_borrowed += 1

        item.save()

        # Whenever borrowed item, send email
        send_mail(
            '{} has borrowed a {}'.format(request.user, item.item_name),
            'Item ID: {}'.format(unborrowed_individual_item.id),
            'noreply@erickdelfin.me',
            ['e_delfin_23@yahoo.com'],
            fail_silently=False
        )

        return render(request, 'inventory/admin.html', {'individual_item': unborrowed_individual_item})


# username = username gotten from user_items urlpattern
def user_items(request, username):
    user = User.objects.get(username=username)

    borrowed_items = ItemBorrowed.objects.filter(user=user, is_returned=False)
    history = ItemBorrowed.objects.filter(user=user, is_returned=True)

    total = len(borrowed_items) + len(history)
    current_borrowed = len(borrowed_items)
    history_count = len(history)

    return render(request, 'inventory/user_items.html', {
        'borrowed_items': borrowed_items,
        'history': history,
        'user': user,
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


# For user register
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready, to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'pic' in request.FILES:
                profile.pic = request.FILES['pic']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            # Login the user
            login(request, user)
            return HttpResponseRedirect("/inventory/")

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    # IN THIS CASE, IT MEANS IT's A 'GET' REQUEST. (See if statement on top = 'POST')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'inventory/registration.html', {
                       'user_form': user_form,
                       'profile_form': profile_form,
                       'registered': registered
                  },
                  context)
