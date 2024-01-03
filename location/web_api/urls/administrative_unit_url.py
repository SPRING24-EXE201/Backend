from django.urls import path

from location.web_api.views import administrative_unit_view

urlpatterns = [
    path('', administrative_unit_view.get_administrative_unit)
]
