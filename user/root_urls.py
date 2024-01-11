from django.urls import path, include

urlpatterns = [
    path('user/', include('user.web_api.urls.user_url')),
]