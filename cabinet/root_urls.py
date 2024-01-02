from django.urls import path, include

urlpatterns = [
    path('cost-version/', include('cabinet.web_api.urls.cost_version_url')),
    path('cabinets/', include('cabinet.web_api.urls.cabinet_url')),
    path('cabinet-types/', include('cabinet.web_api.urls.cabinet_type_url')),
    path('controllers/', include('cabinet.web_api.urls.controller_url')),
]