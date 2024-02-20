from django.urls import path
from . import views

urlpatterns = [
    path('/purchase', views.purchase, name='purchase'),
    path('/box-event', views.box_event, name='box_event'),
]