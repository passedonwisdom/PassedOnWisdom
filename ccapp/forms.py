from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Seller , Customer


class SellerForm(forms.ModelForm):
    Password=forms.CharField(widget=forms.PasswordInput)
    Confirm=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Seller
        fields = ['username','email', 'fullName','Password','Confirm','contactNumber','year', 'branch']


class CustomerForm(forms.ModelForm):
    Password=forms.CharField(widget=forms.PasswordInput)
    Confirm=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['username','email', 'fullName','Password','Confirm','contactNumber','year', 'branch']
