from django.urls import path, include

urlpatterns = [
    path('user/', include('user.web_api.urls.user_url')),
    path('register/', include('user.web_api.urls.register_url')),
    path('login/', include('user.web_api.urls.login_url')),
    path('confirm-otp/', include('user.web_api.urls.otp_confirm_url'))
]