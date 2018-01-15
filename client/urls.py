from django.conf.urls import url
from django.views import generic
import client.views as client_views

app_name = 'client'

urlpatterns = [
    url(r'^$', client_views.personal_info, name='personal_info'),
    url(r'^profile', client_views.profile, name='profile'),
    url(r'^contact', client_views.contact, name='contact'),
    url(r'^picture', client_views.picture, name='picture'),
    url(r'^password', client_views.password, name='password'),

    # url(r'^create_account', client_views.create_account, name='create_account'),
    # url(r'^delete_account', client_views.delete_account, name='delete_account'),
    # url(r'^reset_account_pass', client_views.reset_account_pass, name='reset_account_pass'),

    url(r'^new_order', client_views.new_order, name='new_order'),
    url(r'^view_order/(?P<pk>[0-9]+)$', client_views.view_order, name='view_order'),
    url(r'^update_order/(?P<pk>[0-9]+)$', client_views.update_order, name='update_order'),

    url(r'^order_list', client_views.order_list, name='order_list'),
    url(r'^status_list', client_views.status_list, name='status_list'),

    url(r'^notification', client_views.notification, name='notification'),
]
