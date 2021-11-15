from django.urls import path
from .views import *

app_name = "ecomapp"
urlpatterns = [
    path("", HomeView.as_view() , name="home"),
    path('About/' , AboutView.as_view() , name = "about"),
    path('Contact/' , ContactView.as_view() , name = "contact"),
]
