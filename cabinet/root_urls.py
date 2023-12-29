from django.urls import path, include

urlpatterns = [
    path('cost-version/', include('cabinet.web_api.urls.cost_version_url')),
    path('cells/', include('cabinet.web_api.urls.cell_url')),
    path('cell-logs/', include('cabinet.web_api.urls.cell_log_url'))
]