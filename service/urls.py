from django.conf.urls import url
from django.views import generic
import service.views as service_views

app_name = 'service'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),

    url(r'^profile', service_views.profile, name='profile'),
    url(r'^contact', service_views.contact, name='contact'),
    url(r'^picture', service_views.picture, name='picture'),
    url(r'^upload_picture', service_views.upload_picture, name='upload_picture'),
    url(r'^save_uploaded_picture', service_views.save_uploaded_picture, name='save_uploaded_picture'),
    url(r'^password', service_views.password, name='password'),

    url(r'^create_account', service_views.create_account, name='create_account'),
    url(r'^delete_account', service_views.delete_account, name='delete_account'),
    url(r'^reset_account_pass', service_views.reset_account_pass, name='reset_account_pass'),
    url(r'^select_manager', service_views.select_manager, name='select_manager'),

    url(r'^new_order', service_views.new_order, name='new_order'),
    url(r'^order_list', service_views.order_list, name='order_list'),
]
