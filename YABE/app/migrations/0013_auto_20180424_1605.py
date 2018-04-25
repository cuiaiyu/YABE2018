# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20180419_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='addr',
            name='email',
            field=models.EmailField(default='yabe@yabe.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.ImageField(default='static/app/images/YABE.png', upload_to=''),
        ),
    ]