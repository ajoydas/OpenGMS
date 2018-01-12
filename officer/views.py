# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from authentication.models import NewUser
from core.models import Order
from officer.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm

__FILE_TYPES = ['zip']


@login_required
def personal_info(request):
    return render(request, 'dashboard/personal_info.html', {'user': request.user})


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
    return render(request, 'dashboard/profile.html', {'form': form})


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
    return render(request, 'dashboard/contact.html', {'form': form})


@login_required
def picture(request):
    user = request.user
    if request.method == 'POST':
        user.profile.profile_picture = request.FILES['picture']
        if user.profile.account_flag == 3:
            user.profile.account_flag = 4
        user.save()
        if user.profile.account_flag != 0:
            return redirect('officer:password')

        return render(request, 'dashboard/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'dashboard/picture.html')


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
    return render(request, 'dashboard/password.html', {'form': form})


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


def delete_account(request):
    return render(request, 'dashboard/delete_account.html')


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


def new_order(request):
    user = request.user
    if request.method == 'POST':
        print("NewOrderForm form submitted")
        form = NewOrderForm(request.POST)
        if form.is_valid():
            print("NewOrderForm form Valid")
            order = Order()
            client_username = form.cleaned_data.get('client_username')
            shipping_address = form.cleaned_data.get('shipping_address')
            client_address = form.cleaned_data.get('client_address')
            if client_username:
                if not User.objects.filter(username=client_username):
                    messages.error(request, 'Client with given username doesn\'t exist.')
                    return render(request, 'dashboard/new_order.html', {'form': form})

                client = User.objects.filter(username=client_username)
                if client.profile.account_type != 0:
                    messages.error(request, 'The given client username is not of a client.')
                    if not shipping_address and client_address is True:
                        messages.error(request, 'Ship is client address is invalid here.')
                    return render(request, 'dashboard/new_order.html', {'form': form})
                order.client = client
                if not shipping_address or client_address is True:
                    order.shipping_address = client.profile.address + ", " + client.profile.city + ", " \
                                             + client.profile.state + ", " + client.profile.country + ", " \
                                             + client.profile.zip_code
                else:
                    order.shipping_address = shipping_address
            else:
                if client_address is True:
                    messages.error(request, 'Ship is client address is invalid here.')
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


def order_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    orders = Order.objects.all()
    return render(request, 'dashboard/order_list.html', {'orderlist': orders})


def account_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    new_user_list = NewUser.objects.all()
    user_list = User.objects.all()
    return render(request, 'dashboard/account_list.html', {'new_user_list':new_user_list,'user_list': user_list})
