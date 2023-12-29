from django.urls import path, include

cabinet_root_urls = [
    path('cost-version/', include('cabinet.web_api.urls.cost_version_url')),
    path('cabinet/', include('cabinet.web_api.urls.cabinet_url')),
    path('cabinet-type/', include('cabinet.web_api.urls.cabinet_type_url')),
    path('controller/', include('cabinet.web_api.urls.controller_url')),
]