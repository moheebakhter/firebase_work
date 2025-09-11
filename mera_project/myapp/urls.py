from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path("",views.contacts, name="con"),
  path('show', views.Showdata, name="show"),
]
