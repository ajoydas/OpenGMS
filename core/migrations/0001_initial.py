# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-25 20:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_status', models.CharField(max_length=50)),
                ('client_name', models.CharField(max_length=50, null=True)),
                ('order_type', models.CharField(max_length=20)),
                ('design', models.CharField(max_length=100)),
                ('deadline', models.DateField()),
                ('quantity', models.IntegerField(default=0)),
                ('budget', models.IntegerField(default=0)),
                ('shipping_address', models.CharField(max_length=300, null=True)),
                ('specification', models.CharField(max_length=300, null=True)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_username', to=settings.AUTH_USER_MODEL)),
                ('submitted_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
