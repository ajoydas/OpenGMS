# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-14 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('username', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('order_date', models.DateField()),
                ('delivery_date', models.DateField()),
                ('action', models.CharField(max_length=100)),
            ],
        ),
    ]
