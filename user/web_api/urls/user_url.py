from rest_framework_simplejwt.views import TokenRefreshView

from user.web_api.views import user_view
from django.urls import path

urlpatterns = [
    path('', user_view.get_user, name='get_user'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]