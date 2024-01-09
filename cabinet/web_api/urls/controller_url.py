from cabinet.web_api.views import controller_view
from django.urls import path

urlpatterns = [
    path('', controller_view.get_controller, name='get_controller'),
]
