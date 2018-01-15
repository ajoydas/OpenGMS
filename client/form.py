from django import forms
from django.contrib.auth.models import User
import datetime

from core.models import Order


class ProfileForm(forms.ModelForm):
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        required=True)
    registration_info = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        required=False)
    website = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    additional_info = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300,
        required=True)

    class Meta:
        model = User
        fields = ['company_name', 'registration_info', 'website', 'additional_info']


class NewOrderForm(forms.ModelForm):
    order_types = (('SHIRT', 'Shirt'), ('PANT', 'Pant'), ('T-SHIRT', 'T-Shirt'))
    order_type = forms.ChoiceField(choices=order_types, required=True)
    design = forms.FileField(required=False)
    deadline = forms.DateField(
        widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}),
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

    class Meta:
        model = Order
        fields = ['order_type', 'design', 'deadline','quantity',
                  'budget', 'client_address', 'shipping_address', 'specification']