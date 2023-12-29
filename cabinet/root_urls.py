from django.urls import path, include

cabinet_root_urls = [
    path('cost-version/', include('cabinet.web_api.urls.cost_version_url')),
    path('campaign/', include('cabinet.web_api.urls.campaign_url')),
    path('campaign-cabinet/', include('cabinet.web_api.urls.campaign_cabinet_url')),
]