# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0028_remove_registerbet_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchregistration',
            name='message',
            field=models.CharField(blank=True, default='Aposta Disponível', max_length=300),
        ),
    ]
