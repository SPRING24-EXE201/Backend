from order.web_api.views import order_view
from django.urls import path

urlpatterns = [
    path('', order_view.get_orders, name='get_orders'),
    path('<str:order_id>/', order_view.get_order_by_id, name='get_order_by_order_id'),
    path('create/', order_view.create_order, name='create_order'),
    path('<str:order_id>/update/', order_view.update_order_by_order_id, name='update_order'),
    path('<str:order_id>/delete', order_view.delete_order_by_order_id, name='delete_order_by_order_id')
]
