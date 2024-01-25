from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', include('user.web_api.urls.user_url')),
    path('register', include('user.web_api.urls.register_url')),
    path('login', include('user.web_api.urls.login_url')),
    path('confirm-otp', include('user.web_api.urls.otp_confirm_url')),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]