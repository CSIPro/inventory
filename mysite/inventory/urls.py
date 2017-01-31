from django.conf.urls import url
from . import views

urlpatterns = [

    # /inventory/
    url(r'^$', views.index, name='index'),

]
