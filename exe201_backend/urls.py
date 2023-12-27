"""
URL configuration for exe201_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cost-version/', include('cabinet.web_api.urls.cost_version_url')),
    path('api/cabinet-type/', include('cabinet.web_api.urls.cabinet_type_url')),
    path('api/controller/', include('cabinet.web_api.urls.controller_url')),
    path('api/cabinet/', include('cabinet.web_api.urls.cabinet_url')),
]
