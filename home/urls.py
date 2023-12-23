from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getData),
    path('update/', views.updateData),
    path('delete/', views.deleteData),
    path('create/', views.createData),
]