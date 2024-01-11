from cabinet.web_api.views import cell_view
from django.urls import path

urlpatterns = [
    path('', cell_view.get_cell)
]
