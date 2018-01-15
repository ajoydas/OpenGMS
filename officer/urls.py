from django.conf.urls import url
from django.views import generic
import officer.views as officer_views

app_name = 'officer'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),
    url(r'^$', officer_views.personal_info, name='personal_info'),
    url(r'^profile', officer_views.profile, name='profile'),
    url(r'^contact', officer_views.contact, name='contact'),
    url(r'^picture', officer_views.picture, name='picture'),
    url(r'^password', officer_views.password, name='password'),

    url(r'^create_account', officer_views.create_account, name='create_account'),
    url(r'^delete_account', officer_views.delete_account, name='delete_account'),
    url(r'^reset_account_pass', officer_views.reset_account_pass, name='reset_account_pass'),

    url(r'^new_order', officer_views.new_order, name='new_order'),
    url(r'^view_order/(?P<pk>[0-9]+)$', officer_views.view_order, name='view_order'),
    url(r'^update_order/(?P<pk>[0-9]+)$', officer_views.update_order, name='update_order'),

    url(r'^account_list', officer_views.account_list, name='account_list'),
    url(r'^order_list', officer_views.order_list, name='order_list'),
    url(r'^status_list', officer_views.status_list, name='status_list'),

    url(r'^notification', officer_views.notification, name='notification'),
]
