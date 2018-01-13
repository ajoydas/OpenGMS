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
    progress = models.IntegerField(default=0)

    # o-> not verified yet , 1-> approved , 2-> rejected
    approved = models.IntegerField(default=0)
    review_note = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'orders'


class OrderHistory(models.Model):
    order = models.ForeignKey(Order)
    client = models.ForeignKey(User, related_name="client_username_history", null=True,
                               on_delete=models.SET_NULL)
    submitted_by = models.ForeignKey(User, related_name="submitted_by_history")
    approved_by = models.ForeignKey(User, related_name="approved_by_history", null=True, on_delete=models.SET_NULL)
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
    progress = models.IntegerField(default=0)

    approved = models.IntegerField(default=0)
    review_note = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'order_histories'

    def __init__(self, order, *args, **kwargs):
        super(OrderHistory, self).__init__(*args, **kwargs)
        self.order = order
        self.client = order.client
        self.submitted_by = order.submitted_by
        self.approved_by = order.approved_by
        self.updated_at = order.updated_at
        self.order_status = order.order_status

        self.client_name = order.client_name
        self.order_type = order.order_type
        self.design = order.design
        self.deadline = order.deadline
        self.quantity = order.quantity
        self.budget = order.budget
        self.shipping_address = order.shipping_address
        self.specification = order.specification
        self.progress = order.progress

        self.approved = order.approved
        self.review_note = order.review_note



