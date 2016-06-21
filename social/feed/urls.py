# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import FeedView, PostDeleteView

app_name = 'feed'
urlpatterns = [
    url(r'^$', FeedView.as_view(), name='feed'),
    url(r'^delete_post/$', PostDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
