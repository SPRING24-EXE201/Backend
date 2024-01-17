from location.web_api.views import location_view
from django.urls import path

urlpatterns = [
    path('', location_view.get_location)
]
