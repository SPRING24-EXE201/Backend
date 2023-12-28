from cabinet.web_api.views import cost_version_view
from django.urls import path

urlpatterns = [
    path('', cost_version_view.get_cost_version, name='get_cost_version'),
]