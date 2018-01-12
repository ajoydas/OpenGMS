# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import NewUser
from core.models import Order
from officer.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Order_List

__FILE_TYPES = ['zip']


@login_required
def personal_info(request):
    return render(request, 'service/personal_info.html', {'user': request.user})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        print("Profile form submitted")
        form = ProfileForm(request.POST)
        if form.is_valid():
            print("Profile form Valid")
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.employee.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.employee.sex = form.cleaned_data.get('sex')
            user.employee.designation = form.cleaned_data.get('designation')
            user.employee.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.employee.about = form.cleaned_data.get('about')

            if user.profile.account_flag == 1:
                user.profile.account_flag = 2
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile is successfully saved.')
            if user.profile.account_flag != 0:
                return redirect('officer:contact')

        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Your profile isn\'t saved.')

    else:
        form = ProfileForm(instance=user, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.employee.date_of_birth,
            'sex': user.employee.sex,
            'designation': user.employee.designation,
            'job_title': user.employee.job_title,
            'email': user.email,
            'about': user.employee.about,
        })
    # form = ProfileForm()
    return render(request, 'service/profile.html', {'form': form})


@login_required
def contact(request):
    # form = ContactForm()
    user = request.user
    if request.method == 'POST':
        print("Contact form submitted")
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Contact form Valid")
            user.profile.address = form.cleaned_data.get('address')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.zip_code = form.cleaned_data.get('zip_code')
            user.profile.phone_num = form.cleaned_data.get('phone_num')
            if user.profile.account_flag == 2:
                user.profile.account_flag = 1
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your contact is successfully saved.')
            if user.profile.account_flag != 0:
                return redirect('officer:picture')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Your contact isn\'t saved.')

    else:
        form = ContactForm(instance=user, initial={
            'address': user.profile.address,
            'city': user.profile.city,
            'state': user.profile.state,
            'country': user.profile.country,
            'zip_code': user.profile.zip_code,
            'phone_num': user.profile.phone_num,
        })
    return render(request, 'service/contact.html', {'form': form})


@login_required
def picture(request):
    user = request.user
    if request.method == 'POST':
        user.profile.profile_picture = request.FILES['picture']
        if user.profile.account_flag == 3:
            user.profile.account_flag = 4
        user.save()
        if user.profile.account_flag != 0:
            return redirect('service:password')

        return render(request, 'service/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'service/picture.html')


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            if user.profile.account_flag == 4:
                user.profile.account_flag = 0
                new_user = NewUser.objects.get(user=user)
                new_user.delete()
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password is successfully changed.')
            return redirect('officer:password')
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Your password isn\'t changed.')
            return redirect('officer:password')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'service/password.html', {'form': form})


def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('user', False)
        email = request.POST.get('email', False)
        account_type = request.POST.get('account_type', False)
        print (username)
        print (email)
        print (account_type)

        account_types = {'Client': 0, 'Technical Officer': 1, 'Service Manager': 2, 'Production Manager': 3}
        if (username != False and email != False and account_type != False):
            if not User.objects.filter(username=username).exists():
                password = User.objects.make_random_password(length=10)
                print("Generated Password " + password)
                user = User.objects.create_user(username=username, email=email, password=password)
                user.profile.account_type = account_types[account_type]
                user.save()
                NewUser(user=user, password=password).save()
                messages.success(request, 'Created account successfully.')
            else:
                messages.error(request, 'Submitted form is not valid. User already exist.')

        else:
            messages.error(request, 'Submitted form is not valid. Try again.')
        return render(request, 'service/create_account.html')
    else:
        return render(request, 'service/create_account.html')


def delete_account(request):
    return render(request, 'service/delete_account.html')


def reset_account_pass(request):
    if request.method == 'POST':
        username = request.POST.get('user', False)
        email = request.POST.get('email', False)
        print (username)
        print (email)

        if username != False and email != False:

            if User.objects.filter(username=username).exists():
                user = User.objects.filter(username=username)
                password = User.objects.make_random_password(length=10)
                print("Generated Password " + password)
                user[0].set_password(password)
                user[0].profile.account_flag = 1
                user[0].save()
                if not NewUser.objects.filter(user=user[0]).exists():
                    NewUser(user=user[0], password=password).save()

                messages.success(request, 'Reset password successful.')
            else:
                messages.error(request, 'Submitted form is not valid. Username doesn\'t exist.')

        else:
            messages.error(request, 'Submitted form is not valid. Try again.')

        return render(request, 'service/reset_account_pass.html')
    else:
        return render(request, 'service/reset_account_pass.html')


def select_manager(request):
    return render(request, 'service/select_manager.html')


def new_order(request):
    form = NewOrderForm()
    return render(request, 'service/new_order.html', {'form': form})


def order_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    orders = Order.objects.all()
    return render(request, 'service/order_list.html', {'orderlist': orders})