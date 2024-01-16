from cabinet.web_api.views import campaign_cabinet_view
from django.urls import path

urlpatterns = [
    path('', campaign_cabinet_view.get_campaign_cabinet, name='get_campaign_cabinet'),
]