# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from Notifications.models import Notifications


def general_notification(request, view):
    user = request.user
    unread = user.notifications.unread()
    __notification = Notifications()
    for msg in unread:
        __notification.from_user = msg.actor
        __notification.to_user = user
        __notification.order = msg.action_object
        __notification.notification_message = msg.verb
        __notification.notification_time = msg.timestamp
        print(msg.timestamp)
        __notification.save()
    all_notifications = Notifications.objects.filter(to_user=user)
    paginator = Paginator(all_notifications, 10)
    page = request.GET.get('page', 1) # returns the 1st page
    try:
        notification_list = paginator.page(page)
    except PageNotAnInteger:
        notification_list = paginator.page(1)
    except EmptyPage:
        notification_list = paginator.page(paginator.num_pages)
    return render(request, view, {
        'unread': unread,
        'notification_list': notification_list
    })