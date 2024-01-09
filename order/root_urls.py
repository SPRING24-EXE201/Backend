from django.urls import path, include

urlpatterns = [
    path('', include('order.web_api.urls.order_url')),
    path('order_detail/', include('order.web_api.urls.order_detail_url'))
]