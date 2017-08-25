
from django.conf.urls import url
from django.views import generic
import officer.views as officer_views
from authentication import form

app_name = 'officer'

urlpatterns = [
    url(r'^dash/$', generic.FormView.as_view(
        form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),
    url(r'^create_account', officer_views.create_account, name='create_account'),
    url(r'^delete_account', officer_views.delete_account, name='delete_account'),
    url(r'^reset_account_pass', officer_views.reset_account_pass, name='reset_account_pass'),
]
