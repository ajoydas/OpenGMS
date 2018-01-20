import pickle

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from sklearn.externals import joblib

from OpenGMS.function_util import group_required
from core.models import Order
from django.conf import settings as django_settings
from datetime import timedelta

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

from django.core.files.storage import default_storage as storage

import numpy as np
import pandas as pd


def get_priority(request):
    orders = Order.objects.filter(Q(client__isnull= False) & Q(progress__lte = 100))
    dataset = pd.DataFrame(data=list(orders.values()))

    file1 = storage.open('ml_models/scaler_X_priority.save', 'rb')
    sc_X = joblib.load(file1 )
    file1.close()

    file2 = storage.open('ml_models/scaler_y_priority.save', 'rb')
    sc_y = joblib.load(file2)
    file2.close()

    total_orders = []
    for i in range(0, len(dataset.index)):
        val = pd.to_datetime(dataset['updated_at'][i]) - pd.to_datetime(dataset['created_at'][i])

        total_order = Order.objects.filter(Q(client=orders[i].client) & Q(progress=100)).count()
        total_orders.append([orders[i].client.id, total_order])

    # Preparing the dataset
    X = np.append(total_orders, dataset[['quantity', 'budget']].values, axis=1)
    X_test = sc_X.transform(X)

    file = storage.open('ml_models/estimator_priority.save', 'rb')
    regressor = pickle.load(file)
    file.close()
    y_pred = sc_y.inverse_transform(regressor.predict(X_test)).sort()
    return render(request, 'service/priority_list.html', {'orderlist': orders, 'estimations': y_pred})


def train_model(requset):
    print("Training the estimator")

    orders = Order.objects.filter(Q(client__isnull= False) & Q(progress=100))
    dataset = pd.DataFrame(data=list(orders.values()))
    durations = []
    total_orders = []
    for i in range(0,len(dataset.index)):
        val = pd.to_datetime(dataset['updated_at'][i]) - pd.to_datetime(dataset['created_at'][i])

        total_order = Order.objects.filter(Q(client = orders[i].client) & Q(progress=100)).count()
        # we are calculating for days now
        print(val.days)
        durations.append([val.days])
        total_orders.append([orders[i].client.id, total_order])


    # Preparing the dataset
    X = np.append( total_orders, dataset[['quantity','budget']].values, axis=1)
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
    file1 = storage.open('ml_models/scaler_X_priority.save', 'wb')
    joblib.dump(sc_X, file1)
    file1.close()

    file2 = storage.open('ml_models/scaler_y_priority.save', 'wb')
    joblib.dump(sc_y, file2)
    file2.close()

    # save the model to disk
    file3 =storage.open('ml_models/estimator_priority.save', 'wb')
    pickle.dump(regressor, file3)
    file3.close()

    # y_pred = sc_y.inverse_transform(regressor.predict(X_test))

    return redirect('service:priority_list')


def train_order(order):

    file1 = storage.open('ml_models/scaler_X_priority.save', 'rb')
    sc_X = joblib.load(file1 )
    file1.close()

    file2 = storage.open('ml_models/scaler_y_priority.save', 'rb')
    sc_y = joblib.load(file2)
    file2.close()

    file = storage.open('ml_models/estimator_priority.save', 'rb')
    regressor = pickle.load(file)
    file.close()

    total_order = Order.objects.filter(Q(client=order.client) & Q(progress=100)).count()
    X_train = np.array([[order.client.id, total_order, order.quantity, order.budget]])
    val = order.updated_at - order.created_at
    y_train = np.array([[val.days]], dtype=np.int32)

    X_train = sc_X.transform(X_train)
    y_train = sc_y.fit_transform(y_train)

    regressor.fit(X_train, y_train)

    # save the scalers to disk
    file1 = storage.open('ml_models/scaler_X_priority.save', 'wb')
    joblib.dump(sc_X, file1)
    file1.close()

    # scaler_file_y = django_settings.MEDIA_ROOT + 'ml_models/scaler_y.save'
    file2 = storage.open('ml_models/scaler_y_priority.save', 'wb')
    joblib.dump(sc_y, file2)
    file2.close()

    # save the model to disk
    file3 = storage.open('ml_models/estimator_priority.save', 'wb')
    pickle.dump(regressor, file3)
    file3.close()
