from django.urls import path

from user.web_api.views import login_view

urlpatterns = [
    path('', login_view.login)
]