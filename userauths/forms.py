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



class DateInput(forms.DateInput):
    input_type = 'date'



class UserKYCForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email" , "readonly": "readonly"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}), required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    company = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Company"}), required=False)

    # data kyc models
    image = forms.ImageField(widget=FileInput, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'date_of_birth', 'company', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone
            self.fields['date_of_birth'].initial = user.date_of_birth
            self.fields['company'].initial = user.company

            if hasattr(user, 'kyc'):
                self.fields['image'].initial = user.kyc.image

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            kyc, created = KYC.objects.get_or_create(user=user)
            kyc.image = self.cleaned_data.get('image')
            kyc.save()
        return user