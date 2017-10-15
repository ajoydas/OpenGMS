# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Order_List(models.Model):
    order_id = models.IntegerField()
    username = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    order_date = models.DateField()
    delivery_date = models.DateField()
    action = models.CharField(max_length=100)
