from django.forms.forms import Form
from django.shortcuts import render,redirect
from django.views.generic import TemplateView , CreateView , View , FormView
from django.urls import reverse_lazy
from .models import *
from .forms import CustomerRegistrationForm , CustomerLoginForm, SellerLoginForm, SellerRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 



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

class ShopView(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context

class CustomerRegistrationView(TemplateView):
    template_name = "register.html"

class LoginView(TemplateView):
    template_name = "login_as.html"

class CustomerLogoutView(View):
    def get(self , request):
        logout(request)
        return redirect("ecomapp:home")

class CustomerLoginView(FormView):
    template_name = "login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:shop")

    def form_valid(self , form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        usr = authenticate(username = uname , password = pword)
        if usr is not None and usr.customer:
            login(self.request , usr)
        else:
            return render(self.request , self.template_name , {"form" : self.form_class , "error" : "Invalid Credentials"})

        return super().form_valid(form)

class CustormerRegisterView(CreateView):
    template_name = "register-customer.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:shop")

    def form_valid(self , form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username , email , password)
        form.instance.user = user
        login(self.request , user)
        return super().form_valid(form)

class SellerRegisterView(CreateView):
    template_name = "register-seller.html"
    form_class = SellerRegistrationForm
    success_url = reverse_lazy("ecomapp:selleradmin")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username , email , password)
        form.instance.user = user
        login(self.request , user)
        return super().form_valid(form)

class SellerLoginView(FormView):
    template_name = "login.html"
    form_class = SellerLoginForm
    success_url = reverse_lazy("ecomapp:selleradmin")

    def form_valid(self , form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        usr = authenticate(username = uname , password = pword)
        if usr is not None and usr.seller:
            login(self.request , usr)
        else:
            return render(self.request , self.template_name , {"form" : self.form_class , "error" : "Invalid Credentials"})

        return super().form_valid(form)
    

class SellerAdminView(TemplateView):
    template_name = "seller-admin.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allproducts'] = Product.objects.all()
        return context

class SearchView(TemplateView):
    template_name = "search.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        context['results'] = results
        return context

class ProductDetailView(TemplateView):
    template_name = "productdetailview.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context['product'] = Product.objects.get(slug = slug)

        return context

class AddToCartView(TemplateView):
    template_name = "addtocartview.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        product_obj = Product.objects.get(id = self.kwargs.get('pro_id'))

        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            #try initilazing the cart object with customer username
            cart = Cart.objects.get(id = cart_id)
            product_already_in_cart = cart.cartproduct_set.filter(product = product_obj)
            if product_already_in_cart.exists():
                cart_product = product_already_in_cart.first()
                cart_product.quantity += 1
                cart_product.subtotal += product_obj.selling_price
                cart_product.save()
                cart.total += product_obj.selling_price
                cart.save()
            else:
                cart_product = CartProduct.objects.create(cart = cart , product = product_obj , rate = product_obj.selling_price , quantity = 1 , subtotal = product_obj.selling_price)
                cart.total += product_obj.selling_price
                cart.save()
        else:
            cart = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart.id
            cart_product = CartProduct.objects.create(cart = cart , product = product_obj , rate = product_obj.selling_price , quantity = 1 , subtotal = product_obj.selling_price)
            cart.total += product_obj.selling_price
            cart.save()
        context['cart'] = cart
        return context

 


class CartView(TemplateView):
    template_name = "cart.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)
            context['cart'] = cart
        else:
            context['cart'] = None
        
        return context

class ManageCartView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self , request , *args , **kwargs):
        
        cp_id = self.kwargs.get("cp_id")
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dec":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rem":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomapp:cart")

class SellerProfileView(TemplateView):
    template_name = "profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['sellerdetails'] = Seller.objects.all()
        return context

class CustomerProfileView(TemplateView):
    template_name = "profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['customerdetails'] = Customer.objects.all()
        return context