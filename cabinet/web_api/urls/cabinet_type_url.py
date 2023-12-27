from cabinet.web_api.views import cabinet_type_view
from django.urls import path


urlpatterns = [
    path('', cabinet_type_view.get_cabinet_type, name='get_cabinet_type'),
]