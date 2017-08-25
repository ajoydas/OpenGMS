# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def create_account(request):
    return render(request, 'dashboard/create_account.html')


def delete_account(request):
    return render(request, 'dashboard/delete_account.html')


def reset_account_pass(request):
    return render(request, 'dashboard/reset_account_pass.html')