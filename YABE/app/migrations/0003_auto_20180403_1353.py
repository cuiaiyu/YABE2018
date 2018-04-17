# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_item_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='datetime',
        ),
        migrations.AddField(
            model_name='biddingitem',
            name='expireDay',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biddingitem',
            name='isSold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.TextField(default='Not Set'),
            preserve_default=False,
        ),
    ]
