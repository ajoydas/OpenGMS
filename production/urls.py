from django.conf.urls import url
from django.views import generic
import production.views as production_views

app_name = 'production'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),

    url(r'^profile', production_views.profile, name='profile'),
    url(r'^contact', production_views.contact, name='contact'),
    url(r'^picture', production_views.picture, name='picture'),
    url(r'^upload_picture', production_views.upload_picture, name='upload_picture'),
    url(r'^save_uploaded_picture', production_views.save_uploaded_picture, name='save_uploaded_picture'),
    url(r'^password', production_views.password, name='password'),

    url(r'^new_order', production_views.new_order, name='new_order'),
    url(r'^order_list', production_views.order_list, name='order_list'),
]
