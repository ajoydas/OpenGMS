# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# from order.models import Order
from core.models import Order

# Create your models here.


class Notifications(models.Model):
    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    order = models.ForeignKey(Order, related_name='+', blank=True, default=1)
    notification_message = models.TextField(max_length=250, null=True)
    notification_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Notifications'
