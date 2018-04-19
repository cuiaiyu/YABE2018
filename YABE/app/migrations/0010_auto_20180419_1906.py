# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-19 23:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_cashback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.YabeUser'),
        ),
        migrations.AlterField(
            model_name='order',
            name='buyer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='buyerid', to='app.YabeUser'),
        ),
        migrations.AlterField(
            model_name='order',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Item'),
        ),
        migrations.AlterField(
            model_name='order',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sellerid', to='app.YabeUser'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fromAddr', to='app.Addr'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='toAddr', to='app.Addr'),
        ),
    ]
