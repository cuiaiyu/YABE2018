# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180403_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biddingrecord',
            name='bidding_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
