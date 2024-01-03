from django.urls import path

from location.web_api.views import administrative_region_view

urlpatterns = [
    path('', administrative_region_view.get_administrative_region)
]
