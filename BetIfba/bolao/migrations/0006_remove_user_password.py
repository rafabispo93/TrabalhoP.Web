# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 12:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0005_auto_20160330_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]
