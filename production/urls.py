from django.conf.urls import url
from django.views import generic
import production.views as production_views

app_name = 'production'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),
    url(r'^$', production_views.personal_info, name='personal_info'),
    url(r'^profile', production_views.profile, name='profile'),
    url(r'^contact', production_views.contact, name='contact'),
    url(r'^picture', production_views.picture, name='picture'),
    url(r'^password', production_views.password, name='password'),

    url(r'^view_order/(?P<pk>[0-9]+)$', production_views.view_order, name='view_order'),
    url(r'^update_order/(?P<pk>[0-9]+)$', production_views.update_order, name='update_order'),

    url(r'^order_list', production_views.order_list, name='order_list'),
    url(r'^status_list', production_views.status_list, name='status_list'),

    url(r'^notification', production_views.notification, name='notification'),
]
