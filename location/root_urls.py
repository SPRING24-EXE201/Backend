from django.urls import path, include

urlpatterns = [
    path('district', include('location.web_api.urls.district_url')),
    path('ward', include('location.web_api.urls.ward_url')),
    path('location/', include('location.web_api.urls.location_url')),
    path('administrative-units', include('location.web_api.urls.administrative_unit_url')),
    path('administrative-regions', include('location.web_api.urls.administrative_region_url')),
    path('provinces', include('location.web_api.urls.province_url')),
]