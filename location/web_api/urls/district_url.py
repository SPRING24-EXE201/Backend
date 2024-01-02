from location.web_api.views import district_view
from django.urls import path

urlpatterns = [
    path('', district_view.get_district)
]
