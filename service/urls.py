from django.conf.urls import url
from django.views import generic
import service.views as service_views

app_name = 'service'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),
    url(r'^$', service_views.personal_info, name='personal_info'),
    url(r'^profile', service_views.profile, name='profile'),
    url(r'^contact', service_views.contact, name='contact'),
    url(r'^picture', service_views.picture, name='picture'),
    url(r'^password', service_views.password, name='password'),

    url(r'^create_account', service_views.create_account, name='create_account'),
    url(r'^delete_account', service_views.delete_account, name='delete_account'),
    url(r'^reset_account_pass', service_views.reset_account_pass, name='reset_account_pass'),
    url(r'^select_manager', service_views.select_manager, name='select_manager'),

    url(r'^new_order', service_views.new_order, name='new_order'),
    url(r'^view_order/(?P<pk>[0-9]+)$', service_views.view_order, name='view_order'),
    url(r'^update_order/(?P<pk>[0-9]+)$', service_views.update_order, name='update_order'),

    url(r'^order_list', service_views.order_list, name='order_list'),
    url(r'^status_list', service_views.status_list, name='status_list'),

    url(r'^notification', service_views.notification, name='notification'),

]
