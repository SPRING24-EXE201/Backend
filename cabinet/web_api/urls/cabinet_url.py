from cabinet.web_api.views import cabinet_view
from django.urls import path

urlpatterns = [
    path('', cabinet_view.get_cabinet, name='get_cabinet'),
    path('cabinets/', cabinet_view.get_cabinet_by_id, name='get_cabinet_detail'),
]