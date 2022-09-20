from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.zero_view, name="zero_view"),
    path('home/', views.home_view, name="home_view"),
    path('login/', views.login_view, name="login_view"),
    path('login-success/', views.login_success_view, name="login_success_view"),
    path('logout/', views.logout_view, name="logout_view")
]
