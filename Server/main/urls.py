from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('Index.html', views.home),
    path('add_device.html', views.addDevice),
    path('remove_device.html', views.removeDevice),
    path('home.html', views.main)
]
