from django.urls import path

from location.web_api.views import ward_view

urlpatterns = [
    path('', ward_view.get_ward)
]
