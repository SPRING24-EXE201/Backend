from cabinet.web_api.views import cabinet_opening_view
from django.urls import path

urlpatterns = [
    path('', cabinet_opening_view.get_cabinet_opening_view),
]
