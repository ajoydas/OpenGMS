from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
import datetime

from core.models import Order


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput,
        help_text="'%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'",
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        required=True,
    )
    user_sex = (('MALE', 'Male'), ('FEMALE', 'Female'))
    sex = forms.ChoiceField(choices=user_sex)
    user_designation = (('SENIOR', 'Senior Officer'), ('JUNIOR', 'Junior Officer'))
    designation = forms.ChoiceField(choices=user_designation)
    job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=True)
    about = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 4}),
        max_length=350,
        required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'sex', 'designation', 'job_title',
                  'email', 'about']


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([
                'Old password doesn\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data


class ContactForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=300,
        required=True)
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True)
    state = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True)
    country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True)
    zip_code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=True)
    phone_num = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}), label="Phone number",
                                 required=False, help_text='+ Country Code 11 digit phone\n'
                                                           'e.g. +8801XXXXXXXXX')

    class Meta:
        model = User
        fields = ['address', 'city', 'state', 'country', 'zip_code', 'phone_num']


class NewOrderForm(forms.ModelForm):
    # client_username = forms.CharField(
    #     label="Client Username",
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50,
    #     required=False)
    client_name = forms.CharField(
        label="Client Name",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    order_types = (('SHIRT', 'Shirt'), ('PANT', 'Pant'), ('T-SHIRT', 'T-Shirt'))
    order_type = forms.ChoiceField(choices=order_types, required=True)
    design = forms.FileField(required=False)
    deadline = forms.DateField(
        widget=forms.DateInput,
        help_text="'%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'",
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        required=True)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=True)
    budget = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=True)
    client_address = forms.BooleanField(label="Ship in Client address", required=False)
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=300,
        required=False)
    specification = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=300,
        required=False)
    order_statuses = (('RECEIVED', 'received'), ('CONFIRMED', 'Confirmed'), ('IN-PRODUCTION', 'In-Production')
                      , ('IN-SHIPMENT', 'In-Shipment'), ('DONE', 'Done'), ('REJECTED', 'Rejected'),)
    order_status = forms.ChoiceField(choices=order_statuses, required=True)

    class Meta:
        model = Order
        fields = ['client_name', 'order_type', 'design', 'deadline',
                  'quantity', 'budget','client_address', 'shipping_address', 'specification']
