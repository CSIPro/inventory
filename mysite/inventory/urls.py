from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [

    # /inventory/
    url(r'^$', views.index, name='index'),

    # /inventory/<item_id>/borrow/
    url(r'^search/$', views.item_search, name='search'),

    # /inventory/<item_id>
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),

    # /inventory/<item_id>/borrow/
    url(r'^(?P<pk>[0-9]+)/borrow/$', views.borrow, name='borrow'),

    # /inventory/<username>/            Stores user's username
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.user_items, name='user_items'),

]
