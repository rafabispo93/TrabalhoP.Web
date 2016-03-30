# -*- coding: utf-8 -*-
from django.db import models

class Users(models.Model):
    login = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(min_lenght=5,max_length=15)
    adm = models.BooleanField(default=false)
