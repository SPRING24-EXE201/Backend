from django.urls import include, path
from location.web_api.views import location_view

urlpatterns = [
    #path('', location_view.get_location),
    path('', location_view.LocationViewSet.as_view({'get': 'list'}), name='location_list'),
]