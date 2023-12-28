from django.urls import path, include

cabinet_root_urls = [
    path('cost-version/', include('cabinet.web_api.urls.cost_version_url')),
]