# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy
import pandas
import datetime

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
from django.core.files.storage import default_storage as storage

from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from notifications.signals import notify

from Notifications.views import general_notification
from OpenGMS.function_util import group_required
from authentication.models import NewUser
from client.form import ProfileForm, NewOrderForm
# Create your views here.
from core.models import Order, OrderHistory
from officer.form import ContactForm, ChangePasswordForm
from django.contrib.auth.models import User

# from .tables import OrderTable


@login_required
@group_required('client_group')
def personal_info(request):
    return render(request, 'client/personal_info.html', {'user': request.user})


@login_required
@group_required('client_group')
def profile(request):
    user = request.user
    if request.method == 'POST':
        print("Profile form submitted")
        form = ProfileForm(request.POST)
        if form.is_valid():
            print("Profile form Valid")
            user.client.company_name = form.cleaned_data.get('company_name')
            user.client.registration_info = form.cleaned_data.get('registration_info')
            user.client.website = form.cleaned_data.get('website')
            user.client.additional_info = form.cleaned_data.get('additional_info')

            if user.profile.account_flag == 1:
                user.profile.account_flag = 2
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile is successfully saved.')
            if user.profile.account_flag != 0:
                return redirect('client:contact')

        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Your profile isn\'t saved.')

    else:
        form = ProfileForm(instance=user, initial={
            'company_name': user.client.company_name,
            'registration_info': user.client.registration_info,
            'website': user.client.website,
            'additional_info': user.client.additional_info,
        })
    # form = ProfileForm()
    return render(request, 'client/profile.html', {'form': form})


@login_required
@group_required('client_group')
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
                return redirect('client:picture')
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
    return render(request, 'client/contact.html', {'form': form})


@login_required
@group_required('client_group')
def picture(request):
    user = request.user
    profile_pictures = 'profile_pictures/'
    if request.method == 'POST':
        _picture = request.FILES['picture']
        user_str = request.user.username + '_' + str(request.user.id) + '.jpg'
        filename = profile_pictures + user_str
        with storage.open(filename, 'wb+') as destination:
            for chunk in _picture.chunks():
                destination.write(chunk)
        destination = storage.open(filename, 'rb+')
        im = Image.open(destination)
        width, height = im.size
        if width > 400:
            new_width = 400
            new_height = 300  # (height * 400) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)

            sfile = BytesIO()
            im.save(sfile, format='JPEG')
            destination.close()

            destination = storage.open(filename, 'wb+')
            destination.write(sfile.getvalue())
            destination.close()

        if user.profile.account_flag == 3:
            user.profile.account_flag = 4

        user.profile.profile_picture = '/profile_pictures/' + user_str
        user.save()

        if user.profile.account_flag != 0:
            return redirect('client:password')

        return render(request, 'client/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'client/picture.html')


@login_required
@group_required('client_group')
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
            return redirect('client:password')
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Your password isn\'t changed.')
            return redirect('client:password')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'client/password.html', {'form': form})


DESIGN_FILE_TYPES = ['zip', 'rar', 'gz']
@login_required
@group_required('client_group')
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
                    return render(request, 'client/new_order.html', {'form': form})
                # order.design.url = str(datetime.now())+file_type
            except MultiValueDictKeyError:
                None

            shipping_address = form.cleaned_data.get('shipping_address')
            client_address = form.cleaned_data.get('client_address')

            order.client = user
            if not shipping_address or client_address is True:
                order.shipping_address = str(user.profile.address) + ", " + str(user.profile.city) + ", " \
                                         + str(user.profile.state) + ", " + str(user.profile.country) + ", " \
                                         + str(user.profile.zip_code)
            else:
                order.shipping_address = shipping_address

            order.submitted_by = user
            order.client_name = user.profile.get_screen_name()
            order.order_type = form.cleaned_data.get('order_type')
            order.deadline = form.cleaned_data.get('deadline')
            order.quantity = form.cleaned_data.get('quantity')
            order.budget = form.cleaned_data.get('budget')
            order.specification = form.cleaned_data.get('specification')
            order.order_status = 'RECEIVED'
            order.save()

            # order_history = OrderHistory(order)
            # order_history.save()

            order_history = OrderHistory()
            order_history.copy(order)
            order_history.save()

            # generate notification for submitter
            msg = "Client : {0} submitted a new order with id:{1}".format(
                               request.user.profile.get_screen_name(), order.id)
            _recipient = User.objects.filter(Q(profile__account_type=1) | Q(profile__account_type=2))
            print(_recipient)
            notify.send(request.user, recipient=_recipient, verb=msg, action_object=order)

            messages.success(request, 'The order is saved successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'client/new_order.html', {'form': form})
    form = NewOrderForm()
    return render(request, 'client/new_order.html', {'form': form})


@login_required()
@group_required('client_group')
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
                    return render(request, 'client/update_order.html', {'form': form, 'order':order})
                # order.design.url = str(datetime.now())+file_type
            except MultiValueDictKeyError:
                None

            shipping_address = form.cleaned_data.get('shipping_address')
            client_address = form.cleaned_data.get('client_address')

            order.client = user
            if not shipping_address or client_address is True:
                order.shipping_address = str(user.profile.address) + ", " + str(user.profile.city) + ", " \
                                         + str(user.profile.state) + ", " + str(user.profile.country) + ", " \
                                         + str(user.profile.zip_code)
            else:
                order.shipping_address = shipping_address

            order.submitted_by = user
            order.client_name = user.profile.get_screen_name()
            order.order_type = form.cleaned_data.get('order_type')
            order.deadline = form.cleaned_data.get('deadline')
            order.quantity = form.cleaned_data.get('quantity')
            order.budget = form.cleaned_data.get('budget')
            order.specification = form.cleaned_data.get('specification')
            order.order_status = prv_order.order_status
            order.save()

            # order_history = OrderHistory(order)
            # order_history.save()

            order_history = OrderHistory()
            order_history.copy(order)
            order_history.save()

            msg = "Client :{0} updated the order with id:{1}".format(
                request.user.profile.get_screen_name(), order.id)
            _recipient = User.objects.filter(Q(profile__account_type=1) | Q(profile__account_type=2))
            print(_recipient)
            notify.send(request.user, recipient=_recipient, verb=msg, action_object=order)
            messages.success(request, 'The order is updated successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'client/update_order.html', {'form': form, 'order':order})

    form = NewOrderForm(instance=Order, initial={
        'order_type' : order.order_type,
        'deadline' : order.deadline,
        'quantity' : order.quantity,
        'budget' : order.budget,
        'shipping_address' : order.shipping_address,
        'specification' : order.specification,
    })
    # print(form)
    return render(request, 'client/update_order.html', {'form': form, 'order':order})


# @login_required()
# @group_required('client_group')
# def view_order(request, pk):
#     order = get_object_or_404(Order, id=pk)
#     return render(request, 'client/view_order.html', {'order': order, 'user':request.user})


@login_required()
@group_required('client_group')
def view_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    graph =  order_graph(order)

    return render(request, 'client/view_order.html', {'order': order,
                                                      'user':request.user, 'graph':graph})


@login_required()
@group_required('client_group')
def order_list(request):
    orders = Order.objects.filter(client = request.user)
    return render(request, 'client/order_list.html', {'orderlist': orders})


@login_required()
@group_required('client_group')
def status_list(request):
    orders = Order.objects.filter(Q(client = request.user) & Q(submitted_by=request.user)).order_by('updated_at')
    return render(request, 'client/status_list.html', {'orderlist': orders})


@login_required()
@group_required('client_group')
def notification(request):
    return general_notification(request ,'client/notification.html')


def order_graph(order):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig = Figure(figsize=(9, 6))
    ax = fig.add_subplot(111)
    data = []

    order_hists = OrderHistory.objects.filter(Q(order= order) & Q(submitted_by__profile__account_type=3)).order_by('updated_at')[:10]

    progresses = []
    dates = []
    for hist in order_hists:
        progresses.append(hist.progress)
        dates.append(hist.updated_at.date())

    x_pos = numpy.arange(len(progresses))
    ax.set_xticklabels(dates, rotation=30)
    ax.set_xticks(x_pos)
    ax.plot(x_pos, progresses , color='b', marker='o')
    ax.set_title('Progress chart of the order')
    ax.set_ylabel('Progress (in %)')
    ax.set_xlabel('Updated No.')
    # handles, labels = ax.get_legend_handles_labels()
    # lgd = ax.legend(handles, labels)
    ax.grid('on')

    canvas = FigureCanvas(fig)
    graph1 = django_settings.MEDIA_URL + 'graphs/' + 'graph_progress.jpg'

    file1 = storage.open('graphs/' + 'graph_progress.jpg', 'wb')
    canvas.print_png(file1)
    file1.close()

    return graph1
