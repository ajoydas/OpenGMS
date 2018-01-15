# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from Notifications.views import general_notification
from OpenGMS.function_util import group_required
from authentication.models import NewUser
from core.models import Order, OrderHistory
from officer.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm


@login_required
@group_required('officer_group')
def personal_info(request):
    return render(request, 'dashboard/personal_info.html', {'user': request.user})


@login_required
@group_required('officer_group')
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
    return render(request, 'dashboard/profile.html', {'form': form})


@login_required
@group_required('officer_group')
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
    return render(request, 'dashboard/contact.html', {'form': form})


# @login_required
# def picture(request):
#     user = request.user
#     if request.method == 'POST':
#         user.profile.profile_picture = request.FILES['picture']
#         if user.profile.account_flag == 3:
#             user.profile.account_flag = 4
#         user.save()
#         if user.profile.account_flag != 0:
#             return redirect('officer:password')
#
#         return render(request, 'dashboard/picture.html')
#     print (user.profile.profile_picture)
#     return render(request, 'dashboard/picture.html')


@login_required
@group_required('officer_group')
def picture(request):
    user = request.user
    profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
    if not os.path.exists(profile_pictures):
        os.makedirs(profile_pictures)
    if request.method == 'POST':
        _picture = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_' + str(request.user.id) + '.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in _picture.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 400:
            new_width = 400
            new_height = 300       # (height * 400) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        if user.profile.account_flag == 3:
            user.profile.account_flag = 4

        user.profile.profile_picture = filename
        user.save()

        if user.profile.account_flag != 0:
            return redirect('officer:password')

        return render(request, 'dashboard/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'dashboard/picture.html')


@login_required
@group_required('officer_group')
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
    return render(request, 'dashboard/password.html', {'form': form})


@login_required()
@group_required('officer_group')
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
        return render(request, 'dashboard/create_account.html')
    else:
        return render(request, 'dashboard/create_account.html')


@login_required()
@group_required('officer_group')
def delete_account(request):
    return render(request, 'dashboard/delete_account.html')


@login_required()
@group_required('officer_group')
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

        return render(request, 'dashboard/reset_account_pass.html')
    else:
        return render(request, 'dashboard/reset_account_pass.html')


DESIGN_FILE_TYPES = ['zip', 'rar', 'gz']
@login_required()
@group_required('officer_group')
def new_order(request):
    user = request.user
    if user.employee.manager_id is None:
        messages.error(request, 'Please be assigned to a Service Manager to continue.')
        form = NewOrderForm()
        return render(request, 'dashboard/new_order.html', {'form': form})

    if request.method == 'POST':
        print("NewOrderForm form submitted")
        form = NewOrderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("NewOrderForm form Valid")
            # order = Order()
            order = form.save(commit=False)
            try:
                order.design = request.FILES['design']
                file_type = order.design.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in DESIGN_FILE_TYPES:
                    messages.error(request, 'Image file must be .zip, .rar or .gz')
                    return render(request, 'dashboard/new_order.html', {'form': form})
                # order.design.url = str(datetime.now())+file_type
            except MultiValueDictKeyError:
                None

            try:
                client_id = request.POST['client_username']
            except MultiValueDictKeyError:
                client_id = -1

            shipping_address = form.cleaned_data.get('shipping_address')
            client_address = form.cleaned_data.get('client_address')
            if client_id > 0:
                if not User.objects.filter(id=client_id):
                    messages.error(request, 'Client with given username doesn\'t exist.')
                    return render(request, 'dashboard/new_order.html', {'form': form})

                client = User.objects.get(id=client_id)
                if client.profile.account_type != 0:
                    messages.error(request, 'The given client username is not of a client.')
                    if not shipping_address and client_address is True:
                        messages.error(request, 'Ship is client address is invalid here.')
                    return render(request, 'dashboard/new_order.html', {'form': form})
                order.client = client
                if not shipping_address or client_address is True:
                    order.shipping_address = str(client.profile.address) + ", " + str(client.profile.city) + ", " \
                                             + str(client.profile.state) + ", " + str(client.profile.country) + ", " \
                                             + str(client.profile.zip_code)
                else:
                    order.shipping_address = shipping_address
            else:
                if client_address is True:
                    messages.error(request, 'Ship in client address is invalid here.')
                    return render(request, 'dashboard/new_order.html', {'form': form})
                else:
                    order.shipping_address = shipping_address

            # design = form.cleaned_data.get('design')
            # order.design = "Hello"

            order.submitted_by = user
            order.client_name = form.cleaned_data.get('client_name')
            order.order_type = form.cleaned_data.get('order_type')
            order.deadline = form.cleaned_data.get('deadline')
            order.quantity = form.cleaned_data.get('quantity')
            order.budget = form.cleaned_data.get('budget')
            order.specification = form.cleaned_data.get('specification')
            order.order_status = form.cleaned_data.get('order_status')
            order.save()
            messages.success(request, 'The order is saved successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'dashboard/new_order.html', {'form': form})
    form = NewOrderForm()
    return render(request, 'dashboard/new_order.html', {'form': form})


@login_required()
@group_required('officer_group')
def update_order(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk)

    if user.employee.manager_id is None:
        messages.error(request, 'Please be assigned to a Service Manager to continue.')
        form = NewOrderForm()
        return render(request, 'dashboard/new_order.html', {'form': form})

    if request.method == 'POST':
        print("Updated Order form submitted")
        form = NewOrderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("Updated Order form Validated")

            prv_order = order
            try:
                order.design = request.FILES['design']
                file_type = order.design.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in DESIGN_FILE_TYPES:
                    messages.error(request, 'Image file must be .zip, .rar or .gz')
                    return render(request, 'dashboard/update_order.html', {'form': form, 'order':order})
                # order.design.url = str(datetime.now())+file_type
            except MultiValueDictKeyError:
                None

            try:
                client_id = request.POST['client_username']
            except MultiValueDictKeyError:
                client_id = -1

            shipping_address = form.cleaned_data.get('shipping_address')
            client_address = form.cleaned_data.get('client_address')
            if client_id > 0:
                if not User.objects.filter(id=client_id):
                    messages.error(request, 'Client with given username doesn\'t exist.')
                    return render(request, 'dashboard/update_order.html', {'form': form, 'order':order})

                client = User.objects.get(id=client_id)
                if client.profile.account_type != 0:
                    messages.error(request, 'The given client username is not of a client.')
                    if not shipping_address and client_address is True:
                        messages.error(request, 'Ship is client address is invalid here.')
                    return render(request, 'dashboard/update_order.html', {'form': form, 'order':order})
                order.client = client
                if not shipping_address or client_address is True:
                    order.shipping_address = str(client.profile.address) + ", " + str(client.profile.city) + ", " \
                                             + str(client.profile.state) + ", " + str(client.profile.country) + ", " \
                                             + str(client.profile.zip_code)
                else:
                    order.shipping_address = shipping_address
            else:
                if client_address is True:
                    messages.error(request, 'Ship in client address is invalid here.')
                    return render(request, 'dashboard/update_order.html', {'form': form, 'order':order})
                else:
                    order.shipping_address = shipping_address

            # design = form.cleaned_data.get('design')
            # order.design = "Hello"

            order.submitted_by = user
            order.client_name = form.cleaned_data.get('client_name')
            order.order_type = form.cleaned_data.get('order_type')
            order.deadline = form.cleaned_data.get('deadline')
            order.quantity = form.cleaned_data.get('quantity')
            order.budget = form.cleaned_data.get('budget')
            order.specification = form.cleaned_data.get('specification')
            order.order_status = form.cleaned_data.get('order_status')
            order.save()

            order_history = OrderHistory(prv_order)
            order_history.save()
            messages.success(request, 'The order is updated successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'dashboard/update_order.html', {'form': form, 'order':order})

    form = NewOrderForm(instance=Order, initial={
        'client_name': order.client_name,
        'order_type' : order.order_type,
        'deadline' : order.deadline,
        'quantity' : order.quantity,
        'budget' : order.budget,
        'shipping_address' : order.shipping_address,
        'specification' : order.specification,
        'order_status': order.order_status
    })
    # print(form)
    return render(request, 'dashboard/update_order.html', {'form': form, 'order':order})


@login_required()
@group_required('officer_group')
def view_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    return render(request, 'dashboard/view_order.html', {'order': order, 'user':request.user})


@login_required()
@group_required('officer_group')
def account_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    new_user_list = NewUser.objects.all()
    user_list = User.objects.all()
    return render(request, 'dashboard/account_list.html', {'new_user_list':new_user_list,'user_list': user_list})


@login_required()
@group_required('officer_group')
def order_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    orders = Order.objects.all()
    return render(request, 'dashboard/order_list.html', {'orderlist': orders})


@login_required()
@group_required('officer_group')
def status_list(request):
    orders = Order.objects.filter(submitted_by=request.user).order_by('updated_at')
    return render(request, 'dashboard/status_list.html', {'orderlist': orders})


@login_required()
@group_required('officer_group')
def notification(request):
    return general_notification(request, 'dashboard/notification.html')