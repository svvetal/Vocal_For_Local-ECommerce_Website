from django import forms
from .models import Customer, Seller,Product, Order
from django.contrib.auth.models import User

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = Customer
        fields = ["username" , "password" , "email" , "full_name" , "address"]

    def __init__(self , *args , **kwargs):
        super (CustomerRegistrationForm , self).__init__(*args , **kwargs)

        self.fields["full_name"].widget.attrs['class'] = 'form-control'
        self.fields["address"].widget.attrs['class'] = 'form-control'

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

    def __init__(self , *args , **kwargs):
        super (CustomerLoginForm , self).__init__(*args , **kwargs)

        self.fields["username"].widget.attrs['class'] = 'form-control'
        self.fields["password"].widget.attrs['class'] = 'form-control'

class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = Seller
        fields = ["username" , "password" , "email" , "full_name" , "address" , "shop_name" , "shop_id"]

    def __init__(self , *args , **kwargs):
        super (SellerRegistrationForm , self).__init__(*args , **kwargs)

        self.fields["full_name"].widget.attrs['class'] = 'form-control'
        self.fields["address"].widget.attrs['class'] = 'form-control'
        self.fields["shop_name"].widget.attrs['class'] = 'form-control'
        self.fields["shop_id"].widget.attrs['class'] = 'form-control'

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError("Customer with this Username already Exists")

        return uname

class SellerLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Seller
        fields = ["username" , "password"]

    def __init__(self , *args , **kwargs):
        super (SellerLoginForm , self).__init__(*args , **kwargs)

        self.fields["username"].widget.attrs['class'] = 'form-control'
        self.fields["password"].widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title" , "slug" , "category" , "description" , "image","marked_price","selling_price","warranty","id","stock"]

    def __init__(self , *args , **kwargs):
        super (ProductForm , self).__init__(*args , **kwargs)

        self.fields["title"].widget.attrs['class'] = 'form-control'
        self.fields["slug"].widget.attrs['class'] = 'form-control'
        self.fields["category"].widget.attrs['class'] = 'form-control'
        self.fields["description"].widget.attrs['class'] = 'form-control'
        self.fields["image"].widget.attrs['class'] = 'form-control'
        self.fields["marked_price"].widget.attrs['class'] = 'form-control'
        self.fields["selling_price"].widget.attrs['class'] = 'form-control'
        self.fields["warranty"].widget.attrs['class'] = 'form-control'
        self.fields["id"].widget.attrs['class'] = 'form-control'
        self.fields["stock"].widget.attrs['class'] = 'form-control'

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by" , "shipping_address" , "mobile" , "email"]

    def __init__(self , *args , **kwargs):
        super (CheckoutForm , self).__init__(*args , **kwargs)

        self.fields["ordered_by"].widget.attrs['class'] = 'form-control'
        self.fields["shipping_address"].widget.attrs['class'] = 'form-control'
        self.fields["mobile"].widget.attrs['class'] = 'form-control'
        self.fields["email"].widget.attrs['class'] = 'form-control'