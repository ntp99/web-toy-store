from django.conf.urls import include, url
from .views import index_view, details_view, review_view

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^(?P<id>\d+)$', details_view, name='details'),
    url(r'^(?P<id>\d+)/review$', review_view, name='review'),
]
