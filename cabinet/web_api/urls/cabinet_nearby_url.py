from cabinet.web_api.views import cabinet_view
from django.urls import path

urlpatterns = [
    path('', cabinet_view.get_cabinet_nearby, name='get_cabinet_nearby'),
]
