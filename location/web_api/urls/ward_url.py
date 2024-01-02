from location.web_api.views import ward_view
from django.urls import path

urlpatterns = [
    path('', ward_view.get_ward)
]
