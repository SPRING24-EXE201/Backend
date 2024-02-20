from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('/purchase', staff_member_required(views.purchase), name='purchase'),
    path('/box-event', staff_member_required(views.box_event), name='box_event'),
]