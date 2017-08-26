
from django.conf.urls import url
from django.views import generic
import officer.views as officer_views

app_name = 'officer'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),

    url(r'^profile', officer_views.profile, name='profile'),
    url(r'^contact', officer_views.contact, name='contact'),
    url(r'^picture', officer_views.picture, name='picture'),
    url(r'^upload_picture', officer_views.upload_picture, name='upload_picture'),
    url(r'^save_uploaded_picture', officer_views.save_uploaded_picture, name='save_uploaded_picture'),
    url(r'^password', officer_views.password, name='password'),

    url(r'^create_account', officer_views.create_account, name='create_account'),
    url(r'^delete_account', officer_views.delete_account, name='delete_account'),
    url(r'^reset_account_pass', officer_views.reset_account_pass, name='reset_account_pass'),

    url(r'^new_order', officer_views.new_order, name='new_order'),
]
