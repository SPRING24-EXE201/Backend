from cabinet.web_api.views import cell_log_view
from django.urls import path

urlpatterns = [
    path('', cell_log_view.get_cell_log)
]
