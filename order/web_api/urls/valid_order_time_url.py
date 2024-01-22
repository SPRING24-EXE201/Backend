from django.urls import path

from order.web_api.views import valid_order_time_view

urlpatterns = [
    path('', valid_order_time_view.check_valid_order_time, name='check_valid_order_time')
]