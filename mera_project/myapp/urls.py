from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path("",views.contacts, name="con"),
  path('show', views.Showdata, name="show"),
  path("delete/<str:id>/", views.delete_contact, name="delete"),
  path("r", views.register, name="reg"),
  path("l", views.Login, name="log"),
  path("d", views.dashboard, name="dashboard"),
]
