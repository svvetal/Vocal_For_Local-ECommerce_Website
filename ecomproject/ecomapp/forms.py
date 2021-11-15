from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.forms import ModelForm

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Customer
        fields = ["username" , "password" , "email" , "full_name" , "address"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError("Customer with this Username already Exists")

        return uname

class CustomerLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Customer
        fields = ["username" , "password"]