from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [

    # /inventory/
    url(r'^$', views.index, name='index'),

    # /inventory/<item_id>
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),

]
