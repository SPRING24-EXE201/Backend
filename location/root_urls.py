from django.urls import path, include

urlpatterns = [
    path('district/', include('location.web_api.urls.district_url')),
    path('ward/', include('location.web_api.urls.ward_url')),
    path('location/', include('location.web_api.urls.location_url')),
   
]