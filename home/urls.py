from . import views
from django.urls import path

urlpatterns = [
    path('cost-version/', views.get_cost_version),
    path('campaign/', views.get_campaign),
    path('campaign-cabinet/', views.get_campaign_cabinet),
    path('location/', views.get_location),
    path('ward/', views.get_ward),
    path('district/', views.get_district),
    path('cabinet-type/', views.get_cabinet_type),
    path('controller/', views.get_controller),
    path('cabinet/', views.get_cabinet),
]
