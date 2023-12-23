from . import views
from django.urls import path

urlpatterns = [
    path('cost-version/', views.get_cost_version),
    path('campaign/', views.get_campaign),
]
