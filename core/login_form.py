from django import forms
from material import *


class LogInForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)

    layout = Layout('username', 'email',)