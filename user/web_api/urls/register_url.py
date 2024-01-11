from django.urls import path

from user.web_api.views import register_view

urlpatterns = [
    path('', register_view.register)
]