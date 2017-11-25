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
from client.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Order_List
# from .tables import OrderTable

# Create your views here.


__FILE_TYPES = ['zip']

@login_required
def personalInfo(request):
    return render(request, 'client/personal_info.html', {'user': request.user})

# @login_required
def profile(request):
    # user = request.user
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST)
    #     if form.is_valid():
    #         user.first_name = form.cleaned_data.get('first_name')
    #         user.last_name = form.cleaned_data.get('last_name')
    #         user.profile.job_title = form.cleaned_data.get('job_title')  # profile is for user profile
    #         user.email = form.cleaned_data.get('email')
    #         user.profile.url = form.cleaned_data.get('url')
    #         user.profile.location = form.cleaned_data.get('location')
    #         user.profile.about = form.cleaned_data.get('about')
    #         user.save()
    #         messages.add_message(request,
    #                              messages.SUCCESS,
    #                              'Your profile was successfully edited.')
    #
    # else:
    #     form = ProfileForm(instance=user, initial={
    #         'job_title': user.profile.job_title,
    #         'url': user.profile.url,
    #         'location': user.profile.location
    #         })
    form = ProfileForm()
    return render(request, 'client/client_profile.html', {'form': form})

#@login_required
def contact(request):
    form = ContactForm()
    return render(request, 'client/client_contact.html', {'form': form})


# @login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:
        pass

    print(uploaded_picture)
    return render(request, 'client/client_picture.html',
                  {'uploaded_picture': uploaded_picture})


# @login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('/picture/')


# @login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('picture/')


# @login_required
def password(request):
    # user = request.user
    # if request.method == 'POST':
    #     form = ChangePasswordForm(request.POST)
    #     if form.is_valid():
    #         new_password = form.cleaned_data.get('new_password')
    #         user.set_password(new_password)
    #         user.save()
    #         update_session_auth_hash(request, user)
    #         messages.add_message(request, messages.SUCCESS,
    #                              'Your password was successfully changed.')
    #         return redirect('password')
    #
    # else:
    #     form = ChangePasswordForm(instance=user)
    form = ChangePasswordForm()
    return render(request, 'client/client_password.html', {'form': form})


# def create_account(request):
#     return render(request, 'dashboard/create_account.html')
#
#
# def delete_account(request):
#     return render(request, 'dashboard/delete_account.html')
#
#
# def reset_account_pass(request):
#     return render(request, 'dashboard/reset_account_pass.html')


def new_order(request):
    form = NewOrderForm()
    return render(request, 'client/client_new_order.html', {'form': form})


def order_list(request):
    return render(request, 'client/order_list.html')


def order_view(request):
    return render(request, 'client/order_view.html')


def order_edit(request):
    form = NewOrderForm()
    return render(request, 'client/order_edit.html', {'form': form})