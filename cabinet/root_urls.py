from django.urls import path, include

urlpatterns = [
    path('cost-version/', include('cabinet.web_api.urls.cost_version_url')),
    path('campaign/', include('cabinet.web_api.urls.campaign_url')),
    path('campaign-cabinet/', include('cabinet.web_api.urls.campaign_cabinet_url')),
    path('cells/', include('cabinet.web_api.urls.cell_url')),
    path('cell-logs/', include('cabinet.web_api.urls.cell_log_url')),
    path('cabinet-opening/', include('cabinet.web_api.urls.cabinet_opening_url')),
    path('cabinet/', include('cabinet.web_api.urls.cabinet_url'))
]