# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0012_auto_20160401_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='_game',
        ),
        migrations.AddField(
            model_name='bet',
            name='_game',
            field=models.ManyToManyField(to='bolao.MatchRegistration'),
        ),
    ]
