from django.contrib import admin
from django.urls import path 
from ui_email import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path ('login',auth_views.LoginView.as_view(), name='login'),
    path ('logout',auth_views.LogoutView.as_view(), name='logout'),


    path('', views.index , name = 'index'),
    path('signup', views.signup , name = 'signup'),
    path('home', views.home , name = 'home'),
    
]