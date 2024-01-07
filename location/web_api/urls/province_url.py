from django.urls import path

from location.web_api.views import province_view

urlpatterns = [
    path('', province_view.get_province)
]
