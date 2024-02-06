from cabinet.web_api.views import cell_assignment_view
from django.urls import path

urlpatterns = [
    path('', cell_assignment_view.get_cell_assignment, name='get_cell_assignment'),
    path('assign/', cell_assignment_view.assign_cell_to_user, name='assign_cell_to_user'),
]