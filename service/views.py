# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

import numpy
import pandas
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from notifications.signals import notify

from Notifications.views import general_notification
from OpenGMS.function_util import group_required
from authentication.models import NewUser, Profile
from core.models import Order, OrderHistory
from officer.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm


@login_required
@group_required('service_group')
def personal_info(request):
    return render(request, 'service/personal_info.html', {'user': request.user})


@login_required
@group_required('service_group')
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
                return redirect('service:contact')

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
@group_required('service_group')
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
                return redirect('service:picture')
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


# @login_required
# def picture(request):
#     user = request.user
#     if request.method == 'POST':
#         user.profile.profile_picture = request.FILES['picture']
#         if user.profile.account_flag == 3:
#             user.profile.account_flag = 4
#         user.save()
#         if user.profile.account_flag != 0:
#             return redirect('service:password')
#
#         return render(request, 'service/picture.html')
#     print (user.profile.profile_picture)
#     return render(request, 'service/picture.html')

@login_required
@group_required('service_group')
def picture(request):
    user = request.user
    profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
    if not os.path.exists(profile_pictures):
        os.makedirs(profile_pictures)
    if request.method == 'POST':
        _picture = request.FILES['picture']
        user_str = request.user.username + '_' + str(request.user.id) + '.jpg'
        filename = profile_pictures + user_str
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

        user.profile.profile_picture = '/profile_pictures/' + user_str
        user.save()

        if user.profile.account_flag != 0:
            return redirect('service:password')

        return render(request, 'service/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'service/picture.html')


@login_required
@group_required('service_group')
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
            return redirect('service:password')
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Your password isn\'t changed.')
            return redirect('service:password')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'service/password.html', {'form': form})


@login_required
@group_required('service_group')
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


@login_required
@group_required('service_group')
def delete_account(request):
    return render(request, 'service/delete_account.html')


@login_required
@group_required('service_group')
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


@login_required
@group_required('service_group')
def select_manager(request):
    if request.method == 'POST':
        keys = request.POST.keys()
        print(keys)
        for key in keys:
            try:
                if int(key):
                    print(key+" "+request.POST[key])
                    tech_manager = get_object_or_404(User, id= key)
                    if tech_manager.profile.account_type == 1:
                        if request.POST[key] == 'SELECT' and tech_manager.employee.manager_id == None:
                            tech_manager.employee.manager_id = request.user.employee.id
                            messages.success(request,"Technical manager of Id:"+key+" assigned successfully.")
                            tech_manager.save()
                        elif request.POST[key] == 'RELEASE' and tech_manager.employee.manager_id == request.user.id:
                            tech_manager.employee.manager_id = None
                            messages.success(request,"Technical manager of Id:"+key+" released successfully.")
                            tech_manager.save()
                    else:
                        messages.error(request,"Technical manager of Id:"+key+" can't be assigned.")

            except Exception:
                None

    managers = Profile.objects.filter(account_type=1)\
        .filter(Q(user__employee__manager_id__isnull=True) | Q(user__employee__manager_id=request.user.employee.id))
    print(managers)

    all_managers = Profile.objects.filter(account_type=1)
    return render(request, 'service/select_manager.html',{'managers':managers, 'all_managers':all_managers})


# def new_order(request):
#     form = NewOrderForm()
#     return render(request, 'service/new_order.html', {'form': form})
#
#
# def update_order(request, pk):
#     form = NewOrderForm()
#     return render(request, 'service/new_order.html', {'form': form})


DESIGN_FILE_TYPES = ['zip', 'rar', 'gz']
@login_required
@group_required('service_group')
def new_order(request):
    user = request.user

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
                    return render(request, 'service/new_order.html', {'form': form})
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
                    return render(request, 'service/new_order.html', {'form': form})

                client = User.objects.get(id=client_id)
                if client.profile.account_type != 0:
                    messages.error(request, 'The given client username is not of a client.')
                    if not shipping_address and client_address is True:
                        messages.error(request, 'Ship is client address is invalid here.')
                    return render(request, 'service/new_order.html', {'form': form})
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
                    return render(request, 'service/new_order.html', {'form': form})
                else:
                    order.shipping_address = shipping_address

            order.submitted_by = user
            order.approved_by = user
            order.approved = 1
            order.review_note = request.POST['review_note']
            order.client_name = form.cleaned_data.get('client_name')
            order.order_type = form.cleaned_data.get('order_type')
            order.deadline = form.cleaned_data.get('deadline')
            order.quantity = form.cleaned_data.get('quantity')
            order.budget = form.cleaned_data.get('budget')
            order.specification = form.cleaned_data.get('specification')
            order.order_status = form.cleaned_data.get('order_status')
            order.save()

            if order.client is not None:
                msg = "An officer created a new order with id:{0} for you".format(order.id)
                _recipient = order.client
                notify.send(user, recipient=_recipient, verb=msg, action_object=order)

            messages.success(request, 'The order is saved successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'service/new_order.html', {'form': form})
    form = NewOrderForm()
    return render(request, 'service/new_order.html', {'form': form})


@login_required()
@group_required('service_group')
def update_order(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk)

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
                    return render(request, 'service/update_order.html', {'form': form, 'order':order})
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
                    return render(request, 'service/update_order.html', {'form': form, 'order':order})

                client = User.objects.get(id=client_id)
                if client.profile.account_type != 0:
                    messages.error(request, 'The given client username is not of a client.')
                    if not shipping_address and client_address is True:
                        messages.error(request, 'Ship is client address is invalid here.')
                    return render(request, 'service/update_order.html', {'form': form, 'order':order})
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
                    return render(request, 'service/update_order.html', {'form': form, 'order':order})
                else:
                    order.shipping_address = shipping_address

            # design = form.cleaned_data.get('design')
            # order.design = "Hello"

            order.submitted_by = user
            order.approved_by = user
            order.approved = 1
            order.review_note = request.POST['review_note']
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

            if prv_order.approved == 0:
                # generate notification for production manager
                msg = "Your changes in Order {0} has been discarded by {1}".format(order.id,
                                                     request.user.profile.get_screen_name())
                _recipient = prv_order.submitted_by
                print ("notify to ")
                print(_recipient)
                notify.send(request.user, recipient=_recipient, verb=msg, action_object=order)

            messages.success(request, 'The order is updated successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'service/update_order.html', {'form': form, 'order':order})

    form = NewOrderForm(instance=Order, initial={
        'client_name': order.client_name,
        'order_type' : order.order_type,
        'deadline' : order.deadline,
        'quantity' : order.quantity,
        'budget' : order.budget,
        'shipping_address' : order.shipping_address,
        'specification' : order.specification,
        'order_status' : order.order_status
    })
    # print(form)
    return render(request, 'service/update_order.html', {'form': form, 'order':order})


@login_required
@group_required('service_group')
def view_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        if '_edit' in request.POST:
            return redirect('service:update_order', pk = pk)
        elif '_histories' in request.POST:
            return redirect('service:history_list_pk', pk=pk)
        elif '_approve' in request.POST:
            order.review_note = request.POST['review_note']
            order.approved = 1
            order.approved_by = request.user
            order.save()

            # generate notification for submitter
            msg = "Your changes in Order {0} has been approved by {1}".format( order.id,
                request.user.profile.get_screen_name())
            _recipient = order.submitted_by
            notify.send(request.user, recipient=_recipient, verb=msg, action_object=order)

        elif '_reject' in request.POST:
            # prv_approved = OrderHistory.objects.filter(Q(order_id=order.id) & Q(approved=1))\
            #     .latest('updated_at')
            # print(prv_approved)

            order.review_note = request.POST['review_note']
            order.approved = 2
            order.approved_by = request.user
            order.save()

            # generate notification for submitter
            msg = "Your changes in Order {0} has been rejected by {1}".format(order.id,
                                                request.user.profile.get_screen_name())
            _recipient = order.submitted_by
            notify.send(request.user, recipient=_recipient, verb=msg, action_object=order)

    return render(request, 'service/view_order.html', {'order': order, 'user':request.user})


@login_required
@group_required('service_group')
def view_order_history(request, pk):
    order_history = get_object_or_404(OrderHistory, id=pk)
    if request.method == 'POST':
        if '_view_order' in request.POST:
            return redirect('service:view_order', pk = order_history.order.id)
        elif '_update_order' in request.POST:
            return redirect('service:update_order', pk= order_history.order.id)
        elif '_revert_order' in request.POST:
            order = order_history.order
            _recipient = order.submitted_by

            order.client = order_history.client
            order.submitted_by = order_history.submitted_by
            order.approved_by = order_history.approved_by
            order.updated_at = order_history.updated_at
            order.order_status = order_history.order_status

            order.client_name = order_history.client_name
            order.order_type = order_history.order_type
            order.design = order_history.design
            order.deadline = order_history.deadline
            order.quantity = order_history.quantity
            order.budget = order_history.budget
            order.shipping_address = order_history.shipping_address
            order.specification = order_history.specification
            order.progress = order_history.progress

            order.approved = order_history.approved
            order.review_note = order_history.review_note
            order.save()

            # generate notification for submitter
            msg = "Your changes in Order {0} has been reverted by {1} to the " \
                  "state of history id:{2}".format(order_history.order.id,
                    request.user.profile.get_screen_name(),order_history.id)
            notify.send(request.user, recipient=_recipient, verb=msg, action_object=order)
            return redirect('service:view_order', pk= order_history.order.id)

    return render(request, 'service/view_order_history.html', {'order': order_history, 'user':request.user})


@login_required
@group_required('service_group')
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'service/order_list.html', {'orderlist': orders})


@login_required
@group_required('service_group')
def history_list(request):
    orders = OrderHistory.objects.all()
    return render(request, 'service/order_history_list.html', {'orderlist': orders})


@login_required
@group_required('service_group')
def history_list_pk(request, pk):
    orders = OrderHistory.objects.filter(order_id=pk)
    return render(request, 'service/order_history_list.html', {'orderlist': orders})


@login_required
@group_required('service_group')
def status_list(request):
    tech_managers = User.objects.filter(employee__manager_id=request.user.employee.id)
    orders = Order.objects.filter(submitted_by=tech_managers).order_by('updated_at')
    return render(request, 'service/status_list.html', {'orderlist': orders})


@login_required
@group_required('service_group')
def notification(request):
    return general_notification(request, 'service/notification.html')


@login_required
@group_required('service_group')
def order_graphs(request):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig = Figure(figsize=(9.5, 5.5))
    ax = fig.add_subplot(111)
    data = []
    # months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
    #           'October', 'November', 'December']
    months = [['January'], ['February'], ['March'], ['April'], ['May'], ['June'], ['July'], ['August'],
              ['September'], ['October'], ['November'], ['December']]
    type_list = ['SHIRT', 'PANT','T-SHIRT']
    this_year = datetime.datetime.now().year
    for i in range(0, 3):
        quantities = []
        for j in range(1, 13):
            order = Order.objects.filter(Q(created_at__month=j) & Q(order_type=type_list[i]) &
                                         Q(created_at__year=this_year))\
                .aggregate(Sum("quantity"))
            quantities.append(int(order['quantity__sum'] or 0))
            print(order)
        data.append(quantities)
    quantity_array = numpy.array(data).transpose()
    quantity_array = numpy.append(months, quantity_array, axis=1)
    pd = pandas.DataFrame(data=quantity_array)
    x_pos = numpy.arange(12)
    ax.set_xticklabels(pd[:][0], rotation=30)
    ax.set_xticks(x_pos)
    # ax.bar(x_pos, pd[:][1], align='center', alpha=0.5)
    ax.plot(x_pos, pd[:][1].astype(float), label='Shirt', color='r', marker='o')
    ax.plot(x_pos, pd[:][2].astype(float), label='Pant', color='g', marker='o')
    ax.plot(x_pos, pd[:][3].astype(float), label='T-Shirt', color='b', marker='o')
    ax.set_title('Total numbers of products ordered per month per type in this year')
    ax.set_ylabel('Numbers of products')
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels)
    ax.grid('on')

    canvas = FigureCanvas(fig)
    graph1 = django_settings.MEDIA_URL + '/graphs/' + 'graph1.jpg'
    canvas.print_png(django_settings.MEDIA_ROOT + '/graphs/' + 'graph1.jpg')


    fig = Figure(figsize=(9.5, 5.5))
    ax = fig.add_subplot(111)
    data = []
    for i in range(0, 3):
        quantities = []
        for j in range(1, 13):
            order = Order.objects.filter(Q(created_at__month=j) & Q(order_type=type_list[i]) &
                                         Q(created_at__year=this_year))\
                .aggregate(Sum("budget"))
            quantities.append(int(order['budget__sum'] or 0))
            print(order)
        data.append(quantities)
    quantity_array = numpy.array(data).transpose()
    quantity_array = numpy.append(months, quantity_array, axis=1)
    pd = pandas.DataFrame(data=quantity_array)
    x_pos = numpy.arange(12)
    ax.set_xticklabels(pd[:][0], rotation=30)
    ax.set_xticks(x_pos)
    # ax.bar(x_pos, pd[:][1], align='center', alpha=0.5)
    ax.plot(x_pos, pd[:][1].astype(float), label='Shirt', color='r', marker='o')
    ax.plot(x_pos, pd[:][2].astype(float), label='Pant', color='g', marker='o')
    ax.plot(x_pos, pd[:][3].astype(float), label='T-Shirt', color='b', marker='o')
    ax.set_title('Total budget per month per type in this year')
    ax.set_ylabel('Total Budget')
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels)
    ax.grid('on')

    canvas = FigureCanvas(fig)
    graph2 = django_settings.MEDIA_URL + '/graphs/' + 'graph2.jpg'
    canvas.print_png(django_settings.MEDIA_ROOT + '/graphs/' + 'graph2.jpg')

    # seaborn.distplot(movies.AudienceRating, bins=30)
    # pyplot.plot(pd[0])
    # pyplot.savefig(django_settings.MEDIA_ROOT+'/graph1.jpg')
    return render(request, 'service/order_graphs.html', {'graph1': graph1, 'graph2': graph2})