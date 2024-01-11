from order.web_api.views import order_view
from django.urls import path

urlpatterns = [
    path('', order_view.order_list, name='orders'),
    path('<str:order_id>/', order_view.order_detail, name='order'),
]