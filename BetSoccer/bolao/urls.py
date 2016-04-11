# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^/index.html', views.index),
    url(r'^login', views.login),
    url(r'^apostar',views.apostar),
]