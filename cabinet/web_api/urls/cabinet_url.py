from cabinet.web_api.views import cabinet_view
from django.urls import path

urlpatterns = [
    # path('', cabinet_view.get_cabinet, name='get_cabinet'),
    path('<int:cabinet_id>/empty-cells', cabinet_view.get_empty_cells)
]
