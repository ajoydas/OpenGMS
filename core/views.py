from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render

from core.form import LogInForm


def home(request):
    if request.user is None:
        return redirect('login')
    return redirect_user(request, request.user)


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
                    redirect_user(request, user)

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


def redirect_user(request, user):
    redirect_dict = {1: 'profile', 2: 'contact', 3: 'picture', 4: 'password'}

    if user.profile.account_type == 0:
        if user.profile.account_flag == 0:  # false if not first time or resetted password
            return redirect('client:personal_info')
        return redirect('client:' + redirect_dict[user.profile.account_flag])

    elif user.profile.account_type == 1:
        if user.profile.account_flag == 0:
            return redirect('officer:personal_info')
        return redirect('officer:' + redirect_dict[user.profile.account_flag])

    elif user.profile.account_type == 2:
        if user.profile.account_flag == 0:
            return redirect('service:personal_info')
        return redirect('service:' + redirect_dict[user.profile.account_flag])

    elif user.profile.account_type == 3:
        if user.profile.account_flag == 0:
            return redirect('production:personal_info')
        return redirect('production:' + redirect_dict[user.profile.account_flag])
    else:
        logout(request)