from django.urls import path
from .views import *

app_name = "ecomapp"
urlpatterns = [
    path("", HomeView.as_view() , name="home"),
    path('About/' , AboutView.as_view() , name = "about"),
    path('Contact/' , ContactView.as_view() , name = "contact"),
    path('register/' , CustomerRegistrationView.as_view() , name = "customerregistration"),
    path('logout/' , CustomerLogoutView.as_view() , name = "customerLogout"),
    path('login/' , LoginView.as_view() , name = "Login"),
    path('login/login-customer/' , CustomerLoginView.as_view() , name = "customerlogin"),
    path('login/login-seller/' , SellerLoginView.as_view() , name = "sellerlogin"),
    path('all-products/' , AllProductsView.as_view() , name = "allproducts"),
    path('shop/' , ShopView.as_view() , name = "shop"),
    path('register/register-customer/' , CustormerRegisterView.as_view() , name = "customerregister"),
    path('register/register-seller/' , SellerRegisterView.as_view() , name = "sellerregister"),
    path('search/',SearchView.as_view(),name="search"),
    path('product/<slug:slug>/',ProductDetailView.as_view(),name="productdetailview"),
    path('add-to-cart-<int:pro_id>/',AddToCartView.as_view(),name="addtocart"),
    path('cart/',CartView.as_view(),name="cart"),
    path('seller-admin/' , SellerAdminView.as_view() , name = "selleradmin"),
    path('manage-cart/<int:cp_id>' , ManageCartView.as_view() , name = "managecart"),
    path('seller-profile/' , SellerProfileView.as_view() , name = "sellerprofile"),
    path('customer-profile/' , CustomerProfileView.as_view() , name = "customerprofile"),
    path('add-product/',AddProductView.as_view(),name="add-product"),
    path('checkout/' , CheckOutView.as_view() , name="checkout"),
]
