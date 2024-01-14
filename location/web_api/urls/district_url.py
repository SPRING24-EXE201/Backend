from django.urls import path

from location.web_api.views import district_view

urlpatterns = [
    path('', district_view.get_district)
]
