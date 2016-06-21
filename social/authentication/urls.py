# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

from .views import ProfileView

app_name = 'authentication'
urlpatterns = [
    url(r'^login/', login, {'template_name': 'authentication/login.html'},
        name='login'),
    url(r'^logout/$', logout_then_login, {'login_url': 'authentication:login'},
        name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]
