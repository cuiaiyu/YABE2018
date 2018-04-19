# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-19 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_review_buyer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cashback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.YabeUser')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Order')),
            ],
        ),
    ]
