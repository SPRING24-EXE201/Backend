from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getData),
    path('update/', views.updateData),
    path('delete/', views.deleteData),
    path('create/', views.createData),
    path('administrative-unit/', views.get_administrative_unit),
    path('province/', views.get_province)
]
