"""origin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from bonds.views import BondsViewSet, HelloWorld
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

bonds_router = DefaultRouter()

bonds_router.register(r"bonds", BondsViewSet, base_name="bonds")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HelloWorld.as_view()),
] + bonds_router.urls
