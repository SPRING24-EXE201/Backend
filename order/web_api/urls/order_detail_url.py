from order.web_api.views import order_detail_view
from django.urls import path

urlpatterns = [
    path('',order_detail_view.get_order_detail, name='get_order_detail'),
]