# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-15 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_type',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zip_code',
            field=models.IntegerField(null=True),
        ),
    ]
