from django.urls import path

from user.web_api.views import user_view

urlpatterns = [
    path('', user_view.update_user, name='update_user')
]
