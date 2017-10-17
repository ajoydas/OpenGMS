import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image

from core.form import LogInForm


def home(request):
    return redirect('login')


def login(request):
    if request.method == 'POST':
        print ("Login form validating.")
        form = LogInForm(request.POST)
        if not form.is_valid():
            print ("Login form is not valid.")
            return render(request, 'core/base_form.html',
                      {'form': LogInForm()})

        else:
            # user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    if user.profile.account_type == 0:
                        if user.profile.account_flag:  # false if not first time or resetted password
                            return redirect('client:profile')
                        return redirect('client:profile')

                    elif user.profile.account_type == 1:
                        if user.profile.account_flag:
                            return redirect('officer:profile')
                        return redirect('officer:profile')

                    elif user.profile.account_type == 2:
                        if user.profile.account_flag:
                            return redirect('service:profile')
                        return redirect('service:profile')

                    elif user.profile.account_type == 3:
                        if user.profile.account_flag:
                            return redirect('production:profile')
                        return redirect('production:profile')

            logout(request)
    else:
        print ("Rendering get form")
        return render(request, 'core/base_form.html',
                      {'form': LogInForm()})
