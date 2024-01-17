from location.web_api.views import location_view
from django.urls import path

urlpatterns = [
    path('', location_view.get_location),
    path('search_query=<str:search_query>&pageSize=<int:pageSize>&page=<int:page>', location_view.get_cabinet_location, name='get_cabinet_location')
]
