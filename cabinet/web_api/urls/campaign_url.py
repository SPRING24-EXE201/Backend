from cabinet.web_api.views import campaign_view
from django.urls import path

urlpatterns = [
    path('', campaign_view.get_campaign, name='get_campaign'),
]