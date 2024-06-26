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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import get_json_file, success_payment

urlpatterns = [
    path('api/v1/', include('location.root_urls')),
    path('api/v1/', include('cabinet.root_urls')),
    path('api/v1/order/', include('order.root_urls')),
    path('api/v1/user/', include('user.root_urls')),
    path('.well-known/assetlinks.json', get_json_file),
    path('payos-purchase/success/<int:payment_order_id>', success_payment),

    # API Schema:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/chart-app/', include('chartapp.urls')),
    path('admin/', admin.site.urls),
]

