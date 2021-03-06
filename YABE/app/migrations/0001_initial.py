# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 04:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street1', models.CharField(max_length=100)),
                ('street2', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=15)),
                ('zipcode', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='BiddingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_increment', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BiddingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BiddingItem')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isVirtual', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=20)),
                ('subcategory', models.CharField(max_length=20)),
                ('picture', models.ImageField(upload_to='')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardNumber', models.CharField(max_length=16)),
                ('type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('rating', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Item')),
            ],
        ),
        migrations.CreateModel(
            name='YabeUser',
            fields=[
                ('yabeusername', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('hasMembership', models.BooleanField()),
                ('isSeller', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.YabeUser'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyerid', to='app.YabeUser'),
        ),
        migrations.AddField(
            model_name='order',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Item'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellerid', to='app.YabeUser'),
        ),
        migrations.AddField(
            model_name='order',
            name='ship_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromAddr', to='app.Addr'),
        ),
        migrations.AddField(
            model_name='order',
            name='ship_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toAddr', to='app.Addr'),
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.YabeUser'),
        ),
        migrations.AddField(
            model_name='biddingrecord',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.YabeUser'),
        ),
        migrations.AddField(
            model_name='biddingitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Item'),
        ),
        migrations.AddField(
            model_name='addr',
            name='holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.YabeUser'),
        ),
    ]
