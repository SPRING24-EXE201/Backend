from order.web_api.views import order_view
from django.urls import path

urlpatterns = [
    path('', order_view.get_orders, name='get_order'),
    path('post/', order_view.create_order, name='create_order'),
    path('put/', order_view.update_order, name='update_order'),
    path('delete/', order_view.delete_all_order, name='delete_order'),
    path('delete/<str:order_id>/', order_view.delete_order_by_order_id, name='delete_order_by_order_id')
]
