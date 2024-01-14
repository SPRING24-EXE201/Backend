from django.urls import include, path

urlpatterns = [
    path('administrative-units/', include('location.web_api.urls.administrative_unit_url')),
    path('administrative-regions/', include('location.web_api.urls.administrative_region_url')),
    path('provinces/', include('location.web_api.urls.province_url')),
    path('locations/', include('location.web_api.urls.location_url'))
]
