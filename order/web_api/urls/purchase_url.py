from django.urls import path

from order.web_api.views import purchase_view

urlpatterns = [
    path('', purchase_view.process_purchase)
]
