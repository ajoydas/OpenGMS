# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-25 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20171017_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
