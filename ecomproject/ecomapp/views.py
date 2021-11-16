from django.forms.forms import Form
from django.shortcuts import render,redirect
from django.views.generic import TemplateView , CreateView , View , FormView
from django.urls import reverse_lazy
from .models import *
from .forms import CustomerRegistrationForm , CustomerLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"

class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self , form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username , email , password)
        form.instance.user = user
        login(self.request , user)
        return super().form_valid(form)

class CustomerLogoutView(View):
    def get(self , request):
        logout(request)
        return redirect("ecomapp:home")

class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self , form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        usr = authenticate(username = uname , password = pword)
        if usr is not None and usr.customer:
            login(self.request , usr)
        else:
            return render(self.request , self.template_name , {"form" : self.form_class , "error" : "Invalid Credentials"})

        return super().form_valid(form)

