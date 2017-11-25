import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image

from core.form import LogInForm


def home(request):
    return redirect('login')


def loginview(request):
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
                    login(request,user)
                    redirect_dict = {1: 'profile', 2: 'contact', 3: 'picture', 4: 'password'}

                    if user.profile.account_type == 0:
                        if user.profile.account_flag == 0:  # false if not first time or resetted password
                            return redirect('client:personal_info')
                        return redirect('client:'+redirect_dict[user.profile.account_flag])

                    elif user.profile.account_type == 1:
                        if user.profile.account_flag == 0:
                            return redirect('officer:personal_info')
                        return redirect('officer:'+redirect_dict[user.profile.account_flag])

                    elif user.profile.account_type == 2:
                        if user.profile.account_flag == 0:
                            return redirect('service:personal_info')
                        return redirect('service:'+redirect_dict[user.profile.account_flag])

                    elif user.profile.account_type == 3:
                        if user.profile.account_flag == 0:
                            return redirect('production:personal_info')
                        return redirect('production:'+redirect_dict[user.profile.account_flag])

                    else:
                        logout(request)
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Please enter valid username & password.")

    print ("Rendering get form")
    return render(request, 'core/base_form.html',
                      {'form': LogInForm()})

def logoutview(request):
    logout(request)
    return redirect('login')