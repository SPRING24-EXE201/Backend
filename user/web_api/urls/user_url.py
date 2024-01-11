from user.web_api.views import user_view
from django.urls import path

urlpatterns = [
    path('', user_view.get_user, name='get_user'),
]