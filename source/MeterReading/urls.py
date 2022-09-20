from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('log/', views.log_en, name="log_en"),
    path('endpoint/', views.endpoint, name="endpoint"),
    path('data-last-24h/', views.data_last_24h_view, name="data-last-24h"),
    path('data-all-time/', views.data_all_time_view, name="data-all-time"),
]