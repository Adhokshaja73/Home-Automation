from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add_device.html', views.addDevice),
    path('remove_device.html', views.removeDevice),
    path('post_message/<str:message>', views.postMessage)
]
