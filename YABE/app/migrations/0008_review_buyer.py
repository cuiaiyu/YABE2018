# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 18:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180416_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='buyer',
            field=models.ForeignKey(default='xunzekun', on_delete=django.db.models.deletion.CASCADE, to='app.YabeUser'),
            preserve_default=False,
        ),
    ]
