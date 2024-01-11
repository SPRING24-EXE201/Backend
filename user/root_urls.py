from django.urls import path, include

urlpatterns = [
    path('register/', include('user.web_api.urls.register_url')),
    path('login/', include('user.web_api.urls.login_url'))
]