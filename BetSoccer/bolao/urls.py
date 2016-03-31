# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^bolao/jogos.html/', views.bolao),
    url(r'^index.html', views.index)
]