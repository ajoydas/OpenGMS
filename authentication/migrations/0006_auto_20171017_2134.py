# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-17 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_newuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='about',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]