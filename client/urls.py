
from django.conf.urls import url
from django.views import generic
import client.views as client_views

app_name = 'client'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),

    url(r'^profile', client_views.profile, name='profile'),
    url(r'^contact', client_views.contact, name='contact'),
    url(r'^picture', client_views.picture, name='picture'),
    url(r'^upload_picture', client_views.upload_picture, name='upload_picture'),
    url(r'^save_uploaded_picture', client_views.save_uploaded_picture, name='save_uploaded_picture'),
    url(r'^password', client_views.password, name='password'),

    # url(r'^create_account', client_views.create_account, name='create_account'),
    # url(r'^delete_account', client_views.delete_account, name='delete_account'),
    # url(r'^reset_account_pass', client_views.reset_account_pass, name='reset_account_pass'),

    url(r'^new_order', client_views.new_order, name='new_order'),
    url(r'^order_list', client_views.order_list, name='order_list'),
]
