from order.web_api.views import order_view
from django.urls import path

urlpatterns = [
    path('', order_view.get_order, name='get_order'),
    path('create/', order_view.create_order, name='create_order'),
    path('update/', order_view.update_order, name='update_order'),
    path('delete/', order_view.delete_order, name='delete_order'),
]
