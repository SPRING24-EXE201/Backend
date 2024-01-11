from django.urls import path

from user.web_api.views import otp_confirm_view

urlpatterns = [
    path('', otp_confirm_view.otp_confirm)
]