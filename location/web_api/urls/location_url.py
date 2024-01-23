from location.web_api.views import location_view
from django.urls import path

urlpatterns = [
    # path('', location_view.get_location),
    path('cabinet', location_view.get_cabinet_location, name='get_cabinet_location')
]
