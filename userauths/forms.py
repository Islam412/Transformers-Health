from django import forms
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from django.forms import ImageField, FileInput, DateInput
from django.contrib.auth.forms import UserChangeForm

from .models import User , KYC


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Last Name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    date_of_birth = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date", "placeholder": "Date of Birth"}))
    company = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Company"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'date_of_birth', 'company', 'password1', 'password2']