# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0021_auto_20160405_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='homeScore',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bet',
            name='visitorScore',
            field=models.IntegerField(default=0),
        ),
    ]
