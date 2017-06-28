from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'results', views.search, name='results'),
    url(r'live', views.live, name='name'),
    url(r'stream', views.stream, name='stream'),
]
