# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


#onlinebookshare> mylibrary> views.py/ model.py
class Order(models.Model):
    client = models.ForeignKey(User, related_name="client_username", null=True,
                               on_delete=models.SET_NULL)
    submitted_by = models.ForeignKey(User, related_name="submitted_by")
    approved_by = models.ForeignKey(User, related_name="approved_by", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50)

    client_name = models.CharField(max_length=50, null=True)
    order_type = models.CharField(max_length=20)
    design = models.FileField(upload_to='designs/', null=True, blank=True)
    deadline = models.DateField()
    quantity = models.IntegerField(default=0)
    budget = models.IntegerField(default=0)
    shipping_address = models.CharField(max_length=300, null=True)
    specification = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'orders'
