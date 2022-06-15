from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('post_message/<str:message>', views.postMessage)
]
