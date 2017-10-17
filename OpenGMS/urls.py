"""preseason3_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views import generic

from core import views as core_views
from core import form as core_form

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    # url(r'^login', generic.FormView.as_view(
    #     form_class=core_form.LogInForm, template_name="core/base_form.html",success_url='loginpost'), name="login"),
    url(r'^login', core_views.login, name='login'),
    # url(r'^login', auth_views.login, {'template_name': 'core/login.html'},
    #     name='login'),
    url(r'^auth/', include('authentication.urls')),
    url(r'^officer/', include('officer.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^production/', include('production.urls')),
    url(r'^service/', include('service.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
