from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<signal_id>[0-9]+)/$', views.signalDetail, name='detail'),
    url(r'^updateRegistry$', views.updateRegistry, name='updateRegistry'),
    url(r'^addNewSignal$', views.updateRegistry, name='addNewSignal'),
]
