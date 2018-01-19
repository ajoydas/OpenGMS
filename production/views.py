# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import pickle
from datetime import timedelta


try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

from django.core.files.storage import default_storage as storage

import numpy as np
import pandas as pd
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from notifications.signals import notify
from sklearn.externals import joblib

from Notifications.views import general_notification
from OpenGMS.function_util import group_required
from authentication.models import NewUser
from core.models import Order, OrderHistory
from officer.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm


# Create your views here.

@login_required
@group_required('production_group')
def personal_info(request):
    return render(request, 'production/personal_info.html', {'user': request.user})


@login_required
@group_required('production_group')
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
                return redirect('production:contact')

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
    return render(request, 'production/profile.html', {'form': form})


@login_required
@group_required('production_group')
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
                return redirect('production:picture')
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
    return render(request, 'production/contact.html', {'form': form})


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
@group_required('production_group')
def picture(request):
    user = request.user


    # profile_pictures = django_settings.MEDIA_ROOT + 'profile_pictures/'
    profile_pictures = 'profile_pictures/'
    # if not storage.exists(profile_pictures):
    #     storage.makedirs(profile_pictures)
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
            new_height = 300       # (height * 400) / width
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
            return redirect('production:password')

        return render(request, 'production/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'production/picture.html')


@login_required
@group_required('production_group')
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
            return redirect('production:password')
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Your password isn\'t changed.')
            return redirect('production:password')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'production/password.html', {'form': form})


DESIGN_FILE_TYPES = ['zip', 'rar', 'gz']
@login_required()
@group_required('production_group')
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
                    return render(request, 'production/update_order.html', {'form': form, 'order':order})
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
                    return render(request, 'production/update_order.html', {'form': form, 'order':order})

                client = User.objects.get(id=client_id)
                if client.profile.account_type != 0:
                    messages.error(request, 'The given client username is not of a client.')
                    if not shipping_address and client_address is True:
                        messages.error(request, 'Ship is client address is invalid here.')
                    return render(request, 'production/update_order.html', {'form': form, 'order':order})
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
                    return render(request, 'production/update_order.html', {'form': form, 'order':order})
                else:
                    order.shipping_address = shipping_address

            # design = form.cleaned_data.get('design')
            # order.design = "Hello"

            order.submitted_by = user
            order.approved_by = user
            order.approved = 1
            order.progress = request.POST['progress']
            order.review_note = request.POST['review_note']
            order.client_name = form.cleaned_data.get('client_name')
            order.order_type = form.cleaned_data.get('order_type')
            order.deadline = form.cleaned_data.get('deadline')
            order.quantity = form.cleaned_data.get('quantity')
            order.budget = form.cleaned_data.get('budget')
            order.specification = form.cleaned_data.get('specification')
            order.order_status = form.cleaned_data.get('order_status')
            order.save()

            order_history = OrderHistory(order)
            order_history.save()

            # train the model using current data
            if(order.progress== 100 and order.progress != prv_order.progress):
                train_order(order)

            if order.client is not None:
                msg = "A production manager updated your order with id:{0}".format(order.id)
                _recipient = order.client
                notify.send(user, recipient=_recipient, verb=msg, action_object=order)

            msg = "Production manager :{0} updated the order with id:{1}".format(
                user.profile.get_screen_name(), order.id)
            _recipient = User.objects.filter(Q(profile__account_type=1) | Q(profile__account_type=2))
            notify.send(user, recipient=_recipient, verb=msg, action_object=order)
            messages.success(request, 'The order is updated successfully.')
        else:
            messages.error(request, 'Order save failed.')
            return render(request, 'production/update_order.html', {'form': form, 'order':order})

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
    return render(request, 'production/update_order.html', {'form': form, 'order':order})


@login_required
@group_required('production_group')
def view_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    return render(request, 'production/view_order.html', {'order': order, 'user':request.user})


@login_required
@group_required('production_group')
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'production/order_list.html', {'orderlist': orders})


@login_required
@group_required('production_group')
def status_list(request):
    tech_managers = User.objects.filter(employee__manager_id=request.user.id)
    orders = Order.objects.filter(submitted_by=tech_managers).order_by('updated_at')
    return render(request, 'production/status_list.html', {'orderlist': orders})


@login_required
@group_required('production_group')
def notification(request):
    return general_notification(request, 'production/notification.html')


@login_required
@group_required('production_group')
def estimate(request, pk):
    order = get_object_or_404(Order, id=pk)
    if order.progress == 100:
        render(request, 'production/estimate.html', {'order': order, 'estimated_date': order.updated_at})

    # train_estimator()

    sc_X = joblib.load(django_settings.MEDIA_ROOT + '/ml_models/scaler_X.save')
    sc_y = joblib.load(django_settings.MEDIA_ROOT + '/ml_models/scaler_y.save')

    X_test = np.array([[order.quantity, order.budget]])
    X_test = sc_X.transform(X_test)

    file = storage.open('/ml_models/estimator.save', 'rb')
    regressor = pickle.load(file)
    file.close()

    y_pred = sc_y.inverse_transform(regressor.predict(X_test))

    estimated_date = order.created_at + timedelta(days=y_pred[0])
    return render(request, 'production/estimate.html', {'order': order,
                                                        'estimated_date': estimated_date})


@login_required
@group_required('production_group')
def estimate_list(request):
    orders = Order.objects.filter(progress__lte=100)
    dataset = pd.DataFrame(data=list(orders.values()))

    file1 = storage.open('ml_models/scaler_X.save', 'rb')
    sc_X = joblib.load(file1 )
    file1.close()

    file2 = storage.open('ml_models/scaler_y.save', 'rb')
    sc_y = joblib.load(file2)
    file2.close()

    X = dataset[['quantity', 'budget']].values
    X_test = sc_X.transform(X)

    file = storage.open('ml_models/estimator.save', 'rb')
    regressor = pickle.load(file)
    file.close()
    y_pred = sc_y.inverse_transform(regressor.predict(X_test))

    return render(request, 'production/estimate_list.html', {'orderlist': orders, 'estimations': y_pred})


@login_required
@group_required('production_group')
def train_estimator(requset):
    print("Training the estimator")

    orders = Order.objects.filter(progress=100)
    dataset = pd.DataFrame(data=list(orders.values()))
    durations = []
    for i in range(0,len(dataset.index)):
        # print(dataset['created_at'][i])
        # print(dataset['updated_at'][i])
        duration = []
        val =  pd.to_datetime(dataset['updated_at'][i] ) - pd.to_datetime(dataset['created_at'][i])
        # we are calculating for days now
        print(val.days)
        duration.append(val.days)
        durations.append(duration)

    # Preparing the dataset
    X = dataset[['quantity','budget']].values
    y = np.array(durations, dtype=np.int32)

    # Splitting the dataset into the Training set and Test set
    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0, random_state = 0)

    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    # X_test = sc_X.transform(X_test)
    sc_y = StandardScaler()
    y_train = sc_y.fit_transform(y_train)
    # y_test = sc_y.transform(y_test)

    # Fitting Random Forest Regression to the dataset
    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(n_estimators=100, random_state=0)
    regressor.fit(X_train, y_train)

    # save the scalers to disk
    # scaler_file_X = django_settings.MEDIA_ROOT + 'ml_models/scaler_X.save'
    file1 = storage.open('ml_models/scaler_X.save', 'wb')
    joblib.dump(sc_X, file1)
    file1.close()

    # scaler_file_y = django_settings.MEDIA_ROOT + 'ml_models/scaler_y.save'
    file2 = storage.open('ml_models/scaler_y.save', 'wb')
    joblib.dump(sc_y, file2)
    file2.close()

    # save the model to disk
    file3 =storage.open('ml_models/estimator.save', 'wb')
    pickle.dump(regressor, file3)
    file3.close()

    # y_pred = sc_y.inverse_transform(regressor.predict(X_test))

    return redirect('production:estimate_list')



def train_order(order):

    file1 = storage.open('ml_models/scaler_X.save', 'rb')
    sc_X = joblib.load(file1 )
    file1.close()

    file2 = storage.open('ml_models/scaler_y.save', 'rb')
    sc_y = joblib.load(file2)
    file2.close()

    file = storage.open('ml_models/estimator.save', 'rb')
    regressor = pickle.load(file)
    file.close()

    X_train = np.array([[order.quantity, order.budget]])
    val = order.updated_at - order.created_at
    y_train = np.array([[val]], dtype=np.int32)

    X_train = sc_X.transform(X_train)
    y_train = sc_y.fit_transform(y_train)

    regressor.fit(X_train, y_train)

    # save the scalers to disk
    file1 = storage.open('ml_models/scaler_X.save', 'wb')
    joblib.dump(sc_X, file1)
    file1.close()

    # scaler_file_y = django_settings.MEDIA_ROOT + 'ml_models/scaler_y.save'
    file2 = storage.open('ml_models/scaler_y.save', 'wb')
    joblib.dump(sc_y, file2)
    file2.close()

    # save the model to disk
    file3 = storage.open('ml_models/estimator.save', 'wb')
    pickle.dump(regressor, file3)
    file3.close()
