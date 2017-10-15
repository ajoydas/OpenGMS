from django import forms
from django.contrib.auth.models import User
import datetime


class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    birth_date = forms.DateField(
        widget=forms.DateInput,
        help_text=datetime.date.today, required=True)
    user_sex = ( ('MALE', 'Male'), ('FEMALE', 'Female') )
    sex = forms.ChoiceField(choices=user_sex)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=True)
    about = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=300,
        required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'sex', 'email', 'about']


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
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)
    zip = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)

    class Meta:
        model = User
        fields = ['address', 'city', 'state', 'country', 'phone', 'zip']


class NewOrderForm(forms.ModelForm):
    client_username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    client_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=True)
    order_types = (('SHIRT', 'Shirt'), ('PANT', 'Pant'), ('T-SHIRT', 'T-Shirt'))
    order_type = forms.ChoiceField(choices=order_types)
    design = forms.FileField()
    deadline = forms.DateField(
        widget=forms.DateInput,
        help_text=datetime.date.today, required=True)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)
    budget = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=300,
        required=True)
    specification = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=300,
        required=True)

    class Meta:
        model = User
        fields = ['client_username', 'client_name', 'order_type', 'design', 'deadline',
                  'quantity', 'budget', 'shipping_address', 'specification']