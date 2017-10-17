# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from authentication.models import Profile, Client, Employee

admin.site.register(Profile)
admin.site.register(Client)
admin.site.register(Employee)



